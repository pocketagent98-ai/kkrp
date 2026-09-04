extends Node
# GameConfig Autoload — loads game configuration from game_bible JSON files

var config: Dictionary = {}

func _ready() -> void:
	_load_config()

func _load_config() -> void:
	var paths = {
		"design": "res://game_bible/design.json",
		"world": "res://game_bible/world.json",
		"characters": "res://game_bible/characters.json",
		"quests": "res://game_bible/quests.json",
		"mechanics": "res://game_bible/mechanics.json",
	}
	for key in paths:
		var path = paths[key]
		if FileAccess.file_exists(path):
			var file = FileAccess.open(path, FileAccess.READ)
			if file:
				var json = JSON.new()
				if json.parse(file.get_as_text()) == OK:
					config[key] = json.data
				file.close()

func get_value(section: String, key: String, default: Variant = null) -> Variant:
	if config.has(section) and config[section].has(key):
		return config[section][key]
	return default

func get_levels() -> Array:
	if config.has("world") and config["world"].has("levels"):
		return config["world"]["levels"]
	return []

func get_game_title() -> String:
	return get_value("design", "title", "Desert Rush")
