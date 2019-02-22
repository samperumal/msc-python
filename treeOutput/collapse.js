$(function () {
    $('#treeContainer').jstree({
        "types": {
            "TTree": {
                "icon": "glyphicon glyphicon-tree-conifer"
            },
            "leaf": {
                "icon": "glyphicon glyphicon-list"
            }
        },
        'plugins': ['sort', 'types'],
        'core': {
            'themes': {
                'name': 'proton',
                'responsive': true
            }
        }
    });
});