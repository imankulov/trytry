var updateStep;

$(function () {
    updateStep(flow_name);
    $(".code-input").live({
        keypress: function (event) {
            if (event.charCode === 0) {
                updateStep(flow_name);
            }
        }
    });
});

updateStep = function (flow_name, code_source) {
    $.getJSON('/' + flow_name + '/', code_source, function (data) {
        flow_name = data.flow_name;
        step_prompt = data.step_prompt;
        progress = data.progress;
        task = data.task;
        $("#flow_name").text(flow_name);
        $(".step_prompt").text(step_prompt);
        $(".text-block").html(task);
        $(".bar").css('width', progress + '%');
        return false;
    });
};