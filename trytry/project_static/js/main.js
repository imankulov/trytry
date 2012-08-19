var updateStep, updateData, prompt,
        url = '/' + flow_url + '/',
        multilineMode = false,
        multilineEnd = false,
        commandArray = [];


$(function () {
    // Now i understand, that i don't understand JavaScript!
    $.getJSON(url, function (data) {
        step_prompt = data.step_prompt;
        prompt = step_prompt;
        updateData(data);
        var terminal = $("#code-block").terminal(function (command, term) {
                var regexp = /^\s*$/,
                    regexp_test = regexp.test(command);
                if (command === 'multiline on') {
                    multilineMode = true;
                    prompt = '[' + step_prompt + '] ';
                    term.set_prompt(prompt);
                    commandArray = [];
                } else if (command === 'multiline off' && !commandArray.length) {
                    multilineMode = false;
                    prompt = step_prompt;
                    term.set_prompt(prompt);
                    commandArray = [];
                } else if (!regexp_test || multilineEnd) {
                    if (!multilineMode || (multilineEnd && regexp_test)) {
                        term.pause();
                        commandArray.push(command);
                        command = commandArray.join('\n');
                        $.post(url, {'command': command}, function (data) {
                            if (data.err_text) {
                                term.error(data.err_text);
                            } else  if (data.ok_text) {
                                term.echo("[[i;#E07B08;#000]" + data.ok_text + "]");
                            }
                            term.echo("\n[[i;#6773E5;#000]" + data.hint + "]");
                            updateData(data);
                            term.set_prompt(prompt);
                            multilineEnd = false;
                            commandArray = [];
                            term.resume();
                        });
                    } else {
                        if (regexp_test) {
                            multilineEnd = false;
                        }
                        commandArray.push(command);
                        term.set_prompt('... ');
                    }
                } else {
                    term.set_prompt('... ');
                    if (commandArray.length) {
                        multilineEnd = true;
                    }
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