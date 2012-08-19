var updateStep, updateData, return_prompt,
    url = '/' + flow_url + '/';

$(function () {
    $.getJSON(url, function (data) {
        step_prompt = data.step_prompt;
        updateData(data);
        var terminal = $("#code-block").terminal(function (command, term) {
                var regexp = /^\s*$/;
                if (!regexp.test(command)) {
                    term.pause();
                    $.post(url, {'command': command}, function (data) {
                        if (data.err_text) {
                            term.error(data.err_text);
                        } else  if (data.ok_text) {
                            term.echo("[[i;#E07B08;#000]" + data.ok_text + "]");
                        }
                        term.echo("\n[[i;#6773E5;#000]" + data.hint + "]");
                        updateData(data);
                        term.resume();
                    });
                }
        }, {
            prompt: step_prompt,
            greetings: 'TryTry Project',
            name: flow_url,
            height: 200,
            tabcompletion: true
        });
    });
    $('.previous').click(function () {
        updateStep('prev');
    });
    $('.next').click(function () {
        updateStep('next');
    });
});

updateData = function (data) {
   $("#flow_url").text(data.flow_url);
   $("#text-block").html(data.task);
   $(".bar").css('width', data.progress + '%');
};

updateStep = function (navigate) {
    $.post(url, {'navigate': navigate}, function (data) {
        updateData(data);
        return false;
    });
};