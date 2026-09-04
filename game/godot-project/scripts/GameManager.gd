extends Node
# GameManager Autoload — manages game state, save/load, level progression

signal level_changed(level: int)
signal coins_changed(coins: int)
signal stars_changed(stars: int)
signal game_over()
signal level_complete(level: int)

var current_level: int = 1
var total_coins: int = 0
var total_stars: int = 0
var total_score: int = 0
var is_paused: bool = false

const SAVE_PATH = "user://save_data.json"

func _ready() -> void:
	load_game()

func next_level() -> void:
	current_level += 1
	if current_level > 5:
		current_level = 1
	level_changed.emit(current_level)
	save_game()

func add_coins(amount: int) -> void:
	total_coins += amount
	coins_changed.emit(total_coins)
	save_game()

func set_stars(stars: int) -> void:
	total_stars += stars
	stars_changed.emit(total_stars)
	save_game()

func add_score(amount: int) -> void:
	total_score += amount
	save_game()

func pause_game() -> void:
	is_paused = true
	get_tree().paused = true

func resume_game() -> void:
	is_paused = false
	get_tree().paused = false

func save_game() -> void:
	var data = {
		"current_level": current_level,
		"total_coins": total_coins,
		"total_stars": total_stars,
		"total_score": total_score,
	}
	var file = FileAccess.open(SAVE_PATH, FileAccess.WRITE)
	if file:
		file.store_string(JSON.stringify(data))
		file.close()

func load_game() -> void:
	if not FileAccess.file_exists(SAVE_PATH):
		return
	var file = FileAccess.open(SAVE_PATH, FileAccess.READ)
	if file:
		var json = JSON.new()
		if json.parse(file.get_as_text()) == OK:
			var data = json.data
			current_level = data.get("current_level", 1)
			total_coins = data.get("total_coins", 0)
			total_stars = data.get("total_stars", 0)
			total_score = data.get("total_score", 0)
		file.close()

func reset_progress() -> void:
	current_level = 1
	total_coins = 0
	total_stars = 0
	total_score = 0
	save_game()
