import json


def build_children(node, parent_node):
	if node["parent_id"] == parent_node["id"]:
		parent_node.setdefault("children", list())
		parent_node["children"].append(node)
		return True
	else:
		for x_node in parent_node.get("children", list()):
			if build_children(node, x_node):
				return True
	return False


def build_tree(records):
	# 构建root
	root = list()
	idx = 0
	while idx < len(records):
		if records[idx]["parent_id"] == 0: # 是根节点
			records[idx].update({"children": list()})
			root.append(records[idx])
			del records[idx]
		else:
			idx += 1

	while len(records) > 0:
		idx = 0
		while idx < len(records):
			node = records[idx]
			found = False
			for parent_node in root:
				found = build_children(node, parent_node)
				if found:
					del records[idx]
					break
			if not found:
				idx += 1
	return root

if __name__ == '__main__':
	from data import records
	root = build_tree(records)
	print(json.dumps(root, indent=4, ensure_ascii=False))