// Array to store the selected directory names.
let dirs = [];
let send_dirs = [];
let confirm_dirs = {};

const close_btn = "<button type='button' class='btn-close' data-bs-dismiss='alert' aria-label='Close' onclick='close_message()'></button>"

// Clear the selected value.
function value_reset() {
    dirs = [];
    send_dirs = [];
    confirm_dirs = [];

    $("#select_now").empty();
    $(".row_group").empty();
    $(".x-axis").empty();
    $("#select_modules").empty();
}

// Display the tree structure and store the selected values in "dirs"
function createJSTree(jsondata) {
    $("#SimpleJSTree").jstree({
        "core": {
            "data": jsondata["data"]
        },
        "types" : {
            "default" : {
                "icon": "far fa-folder",
                "leaf": "far fa-folder"
            }
        },
        "search": {
            "case_insensitive": true,
            "show_only_matches": true
        },
        "plugins" : [
            "themes", 
            "json_data", 
            "ui", 
            "types", 
            "wholerow",
            "search",
            "contentmenu",
            "dnd",
            "state"
        ],
    })  
    .on("changed.jstree", function (e, data) {
        for (let i = 0; i < data.selected.length; i++) {
            dirs.push(data.instance.get_node(data.selected[i]).text);
            send_dirs.push(data.instance.get_node(data.selected[i]).id);
        }
        $("#select_now").empty();
        for (let i = 0; i < dirs.length; i++) {
            $("#select_now").append("<li class='list-group-item'>" + dirs[i] + "</li>");
        }
    })
    .on("search.jstree", function (nodes, str, res) {
        if (str.nodes.length === 0) {
            $("#deliverables").jstree(true).hide_all()
        }
    })
}
$('#deliverable_search').keyup(function () {
    $('#SimpleJSTree').jstree(true).show_all();
    $('#SimpleJSTree').jstree('search', $(this).val());
});            

// close message function
function close_message() {
    $(".message").empty();
}

function confirm() {
    let version_checkbox = $("input:checkbox[name='version']:checked").val()

    if (version_checkbox == "") {
        version_checkbox = true
    } else {
        version_checkbox = false
    }
    
    $.ajax("/confirm", {
        type: "POST",
        dataType: "json",
        data: {
                "language": $("input:radio[name='lang']:checked").val(),
                "dir_list": send_dirs.join(','),
                "version": version_checkbox
            },
    }).done(function (data) {
        $("#select_modules").empty()
        $(".message").empty()

        let module_empty_directories = []
        const result = JSON.parse(data.values)

        let include_modules_directories_count = 0
        Object.keys(result).forEach(function (value) {
            confirm_dirs[include_modules_directories_count] = value
            
            if (result[value].length == 0) {
                module_empty_directories.push(value)
            } else {
                $("#select_modules").append("<p class='h6 mt-3'>" + value + "</p>")
                for (let i = 0; i < result[value].length; i++) {
                    $("#select_modules").append(
                    "<div class='form-check'><input name='xxx" + include_modules_directories_count + "' class='form-check-input' type='checkbox' value='" + 
                    result[value][i] + "' id='module' checked>" + 
                    "<label class='form-check-label' for='module'>" + result[value][i] + "</label></div>")
                }
                include_modules_directories_count += 1
            }
        })
        let message = module_empty_directories.join(", ")

        if (send_dirs.length == 0) {
            $(".message").append("<div class='alert alert-danger alert-dismissible fade show' role='alert'>No directory selected!" + close_btn + "</div>")
        } else {
            if (module_empty_directories.length >= 1 && include_modules_directories_count == 0) {
                $(".message").append("<div class='alert alert-info alert-dismissible fade show' role='alert'>Could not find a module to write to requirements.txt.<br>" + message + close_btn + "</div>")
            } else if (module_empty_directories.length == 0 && include_modules_directories_count >= 1) {
                $("#select_modules").append("<div style='float: right;'><button type='button' class='btn btn-dark' onclick='generate()'>OK</button></div>")
            } else if (module_empty_directories.length >= 1 && include_modules_directories_count >= 1) {
                $(".message").append("<div class='alert alert-info alert-dismissible fade show' role='alert'>Could not find a module to write to requirements.txt.<br>" + message + close_btn + "</div>")
                $("#select_modules").append("<div style='float: right;'><button type='button' class='btn btn-dark' onclick='generate()'>OK</button></div>")
            }
        }
    })
}

// Function to send data to the backend(Main Function)
function generate() {
    let result = {}

    Object.keys(confirm_dirs).forEach(function (value) {
        result[confirm_dirs[value]] = []
        const tmp = document.getElementsByName("xxx" + parseInt(value))

        for (let i = 0; i < tmp.length; i++) {
            if (tmp[i].checked) {
                result[confirm_dirs[value]].push(tmp[i].value);
            }
        }
    })

    if (dirs.length >= 1) {
        $.ajax("/generate", {
            type: "POST",
            data: {
                "language": $("input:radio[name='lang']:checked").val(),
                "confirmed_data": JSON.stringify(result)
            },
            dataType: "json",
        }).done(function (data) {
            const message = "Generate successful!"

            value_reset()
            $("#select_modules").empty();
            $(".message").empty();
            $(".message").append("<div class='alert alert-success alert-dismissible fade show' role='alert'>" + message + close_btn + "</div>");
        }).fail(function (data) {
            const message = "Generate failed!"

            $("#select_modules").empty();
            $(".message").empty();
            $(".message").append("<div class='alert alert-danger alert-dismissible fade show' role='alert'>" + message + close_btn + "</div>");
        });
    } else {
        const message = "No directory selected!"

        $(".message").empty();
        $(".message").append("<div class='alert alert-danger alert-dismissible fade show' role='alert'>" + message + close_btn + "</div>");
    }
}

// update directory information
function update() {
    $.ajax("/update", {
        type: "POST",
        dataType: "json",
    }).done(function (data) {
        const message = "Update directory successful!"
        
        $(".message").empty();
        $(".message").append("<div class='alert alert-success alert-dismissible fade show' role='alert'>" + message + close_btn + "</div>");
        
        location.reload();
    }).fail(function (data) {
        const message = "Update directory failed!"
        
        $(".message").empty();
        $(".message").append("<div class='alert alert-danger alert-dismissible fade show' role='alert'>" + message + close_btn + "</div>");
    });
}
// get detail
function detail() {
    $.ajax("/detail", {
        type: "POST",
        dataType: "json",
        data: {
            "dir_list": send_dirs.join(',')
        }
    }).done(function (data) {
        const result = JSON.parse(data.values)
        $(".row_group").empty();
        $(".x-axis").empty();

        Object.keys(result).forEach(function (value) {
            let path = value;
            let python = 0;
            let julia = 0;
            let go = 0;
            let ipynb = 0;
            let other = 0;

            Object.keys(this[value]).forEach(function (value) {
                switch (value) {
                    case "py":
                        python = this[value];
                    case "jl":
                        julia = this[value];
                    case "go":
                        go = this[value];
                    case "ipynb":
                        ipynb = this[value];
                    case "other":
                        other = this[value];
                }
            }, this[value])

            $(".row_group").append("<div class='row'><h6>"
                + value + "</h6><div class='chart'><span class='block' title='Python' style='width:" + python + "%;'><span class='value'>"
                + python + "%</span></span><span class='block' title='Julia' style='width:" + julia + "%;'><span class='value'>"
                + julia + "%</span></span><span class='block' title='Go' style='width:" + go + "%;'><span class='value'>"
                + go + "%</span></span><span class='block' title='Ipynb' style='width:" + ipynb + "%;'><span class='value'>"
                + ipynb + "%</span></span><span class='block' title='Other' style='width:" + other + "%;'><span class='value'>"
                + other + "%</span></span></div></div>");
        }, result)

        $(".x-axis").append("<h3>Languages</h3><ul class='legend'><li>Python</li><li>Julia</li><li>Go</li><li>Ipynb</li><li>Ohter</li></ul>");
    })
}
