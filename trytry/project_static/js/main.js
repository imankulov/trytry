var updateStep, return_prompt;

$(function () {
    $.getJSON('/' + flow_name + '/', function (data) {
        step_prompt = data.step_prompt;
        $("#flow_name").text(data.flow_name);
        $("#text-block").html(data.task);
        $(".bar").css('width', data.progress + '%');
        var terminal = $("#code-block").terminal(function (command, term) {
                var regexp = /^\s*$/,
                    url = '/' + flow_name + '/';
                if (!regexp.test(command)) {
                    $.post(url, {'command': command}, function (data) {
                        if (data.err_text) {
                            term.error(data.err_text);
                        } else {
                            term.echo("[[i;#E07B08;#000]" + data.ok_text + "]");
                        }
                        term.echo("\n[[i;#6773E5;#000]" + data.hint + "]");
                        $("#flow_name").text(data.flow_name);
                        $("#text-block").html(data.task);
                        $("#bar").css('width', data.progress + '%');
                    });
                }
        }, {
            prompt: step_prompt,
            greetings: 'TryTry Project',
            name: flow_name,
            height: 200,
            tabcompletion: true
        });
    });
});

updateStep = function (flow_name, code_text) {
    var url = '/' + flow_name + '/';
    if (code_text) {
        $.post(url, {'command': code_text}, function (data) {
            $("#flow_name").text(data.flow_name);
            $("#text-block").html(data.task);
            $("#bar").css('width', data.progress + '%');
        });
    } else {
        $.getJSON(url, function (data) {
            $("#flow_name").text(data.flow_name);
            $("#text-block").html(data.task);
            $("#bar").css('width', data.progress + '%');
            return false;
        });
    }
};