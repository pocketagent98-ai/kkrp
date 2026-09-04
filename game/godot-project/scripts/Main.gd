extends Node3D

# Desert Rush — Main Game Script (GDScript for Godot 4.7.2)
# 3D 3-lane runner: player car, obstacles, coins, star ratings, timer
# Reads config from GameConfig autoload

var current_level: int = 1
var max_levels: int = 5
var time_left: float = 60.0
var coins_collected: int = 0
var stars: int = 3
var game_speed: float = 0.30
var player_z: float = 5.0
var player_lane: int = 1
var target_x: float = 0.0
var is_jumping: bool = false
var jump_vel: float = 0.0
var road_length: float = 200.0
var lane_positions: Array[float] = [-2.0, 0.0, 2.0]

var player: CharacterBody3D
var camera: Camera3D
var sun: DirectionalLight3D
var ground: MeshInstance3D
var finish_line: MeshInstance3D
var obstacles: Array[Node3D] = []
var coin_objects: Array[Node3D] = []

const LEVELS = [
	{"time": 60, "speed": 0.30, "type": "desert", "obstacles": 15, "coins": 20, "name": "Desert Dawn"},
	{"time": 55, "speed": 0.35, "type": "desert", "obstacles": 20, "coins": 25, "name": "Sand Storm"},
	{"time": 50, "speed": 0.40, "type": "transition", "obstacles": 25, "coins": 30, "name": "Desert to City"},
	{"time": 45, "speed": 0.45, "type": "city", "obstacles": 30, "coins": 35, "name": "City Rush"},
	{"time": 40, "speed": 0.50, "type": "city", "obstacles": 35, "coins": 40, "name": "Singapore Skyline"},
]

func _ready() -> void:
	randomize()
	_init_level(current_level)

func _init_level(level: int) -> void:
	var config = LEVELS[level - 1]
	time_left = float(config.time)
	game_speed = config.speed
	coins_collected = 0
	stars = 3
	player_lane = 1
	target_x = 0.0
	player_z = 5.0
	_build_world(config.type, config)
	_create_player()
	_setup_camera(config.type)
	print("Level %d: %s" % [level, config.name])

func _build_world(world_type: String, config: Dictionary) -> void:
	var road_geom = PlaneMesh.new()
	road_geom.size = Vector2(8, road_length)
	var road_mat = StandardMaterial3D.new()
	if world_type == "desert" or world_type == "transition":
		road_mat.albedo_color = Color(0.83, 0.63, 0.37)
	else:
		road_mat.albedo_color = Color(0.2, 0.2, 0.27)
	ground = MeshInstance3D.new()
	ground.mesh = road_geom
	ground.material_override = road_mat
	ground.position = Vector3(0, 0, -road_length / 2 + 10)
	ground.rotation.x = -PI / 2
	add_child(ground)
	sun = DirectionalLight3D.new()
	sun.position = Vector3(20, 30, 10)
	sun.rotation.x = -PI / 4
	sun.light_energy = 1.2 if world_type != "city" else 0.6
	sun.shadow_enabled = true
	add_child(sun)
	for i in range(config.obstacles):
		var lane = randi() % 3 - 1
		var z_pos = -10.0 - i * (road_length / config.obstacles) - randf() * 3
		var obs = _create_obstacle(lane, z_pos, world_type)
		obstacles.append(obs)
		add_child(obs)
	for i in range(config.coins):
		var lane = randi() % 3 - 1
		var z_pos = -5.0 - i * (road_length / config.coins) - randf() * 3
		var coin = _create_coin(lane, z_pos)
		coin_objects.append(coin)
		add_child(coin)
	var finish_geom = PlaneMesh.new()
	finish_geom.size = Vector2(8, 2)
	var finish_mat = StandardMaterial3D.new()
	finish_mat.albedo_color = Color.WHITE
	finish_mat.transparency = BaseMaterial3D.TRANSPARENCY_ALPHA
	finish_line = MeshInstance3D.new()
	finish_line.mesh = finish_geom
	finish_line.position = Vector3(0, 0.02, -road_length + 5)
	finish_line.rotation.x = -PI / 2
	add_child(finish_line)

func _create_obstacle(lane: int, z_pos: float, world_type: String) -> Node3D:
	var obs = MeshInstance3D.new()
	if world_type == "desert":
		var box = BoxMesh.new()
		box.size = Vector3(0.8, 0.6, 1.2)
		obs.mesh = box
		var mat = StandardMaterial3D.new()
		mat.albedo_color = Color(0.55, 0.27, 0.07)
		obs.material_override = mat
		obs.position = Vector3(lane_positions[lane + 1], 0.3, z_pos)
	else:
		var cone = PrismMesh.new()
		cone.size = Vector3(0.8, 0.8, 0.8)
		obs.mesh = cone
		var mat = StandardMaterial3D.new()
		mat.albedo_color = Color(0.91, 0.27, 0.27)
		obs.material_override = mat
		obs.position = Vector3(lane_positions[lane + 1], 0.4, z_pos)
	obs.set_meta("type", "obstacle")
	obs.set_meta("lane", lane)
	return obs

func _create_coin(lane: int, z_pos: float) -> Node3D:
	var coin = MeshInstance3D.new()
	var cyl = CylinderMesh.new()
	cyl.top_radius = 0.3
	cyl.bottom_radius = 0.3
	cyl.height = 0.08
	coin.mesh = cyl
	var mat = StandardMaterial3D.new()
	mat.albedo_color = Color(0.96, 0.65, 0.14)
	mat.emission_enabled = true
	mat.emission = Color(0.96, 0.65, 0.14)
	mat.emission_energy_multiplier = 0.5
	mat.metallic = 0.7
	mat.roughness = 0.3
	coin.material_override = mat
	coin.position = Vector3(lane_positions[lane + 1], 1.0, z_pos)
	coin.rotation.x = PI / 2
	coin.set_meta("type", "coin")
	coin.set_meta("collected", false)
	coin.set_meta("lane", lane)
	return coin

func _create_player() -> void:
	player = CharacterBody3D.new()
	var body_mesh = BoxMesh.new()
	body_mesh.size = Vector3(0.8, 0.5, 1.5)
	var body = MeshInstance3D.new()
	body.mesh = body_mesh
	var body_mat = StandardMaterial3D.new()
	body_mat.albedo_color = Color(0.91, 0.27, 0.27)
	body_mat.metallic = 0.5
	body_mat.roughness = 0.3
	body.material_override = body_mat
	body.position.y = 0.5
	player.add_child(body)
	var col = CollisionShape3D.new()
	var shape = BoxShape3D.new()
	shape.size = Vector3(0.8, 0.5, 1.5)
	col.shape = shape
	player.add_child(col)
	player.position = Vector3(0, 0, 5)
	add_child(player)

func _setup_camera(world_type: String) -> void:
	if not camera:
		camera = Camera3D.new()
		add_child(camera)
	camera.position = Vector3(0, 6, 10)
	camera.rotation.x = -0.5

func _process(delta: float) -> void:
	if not player:
		return
	player_z -= game_speed
	player.position.z = player_z
	player.position.x = lerp(player.position.x, target_x, 0.2)
	if is_jumping:
		player.position.y += jump_vel
		jump_vel -= 0.015
		if player.position.y <= 0:
			player.position.y = 0
			is_jumping = false
			jump_vel = 0
	camera.position.x = player.position.x * 0.5
	camera.position.z = player_z + 10
	camera.look_at(Vector3(player.position.x * 0.3, 1, player_z - 10))
	time_left -= delta
	if time_left <= 0:
		_game_over()
	for coin in coin_objects:
		if coin.get_meta("collected"):
			continue
		var dx = coin.position.x - player.position.x
		var dz = coin.position.z - player.position.z
		if abs(dx) < 0.8 and abs(dz) < 1.0:
			coin.set_meta("collected", true)
			coin.visible = false
			coins_collected += 1
	for obs in obstacles:
		var dx = obs.position.x - player.position.x
		var dz = obs.position.z - player.position.z
		if abs(dx) < 0.8 and abs(dz) < 1.0 and player.position.y < 0.8:
			player_z += 2.0
			stars = max(0, stars - 1)
	if player_z < -road_length + 10:
		_level_complete()

func _input(event: InputEvent) -> void:
	if event.is_action_pressed("move_left"):
		if player_lane > 0:
			player_lane -= 1
			target_x = lane_positions[player_lane]
	elif event.is_action_pressed("move_right"):
		if player_lane < 2:
			player_lane += 1
			target_x = lane_positions[player_lane]
	elif event.is_action_pressed("jump"):
		if not is_jumping:
			is_jumping = true
			jump_vel = 0.25
	elif event.is_action_pressed("pause"):
		get_tree().paused = !get_tree().paused

func _level_complete() -> void:
	print("Level %d Complete! Stars: %d, Coins: %d" % [current_level, stars, coins_collected])
	current_level += 1
	if current_level > max_levels:
		print("All levels complete!")
		current_level = 1
	_init_level(current_level)

func _game_over() -> void:
	print("Game Over! Coins: %d" % coins_collected)
	_init_level(current_level)
