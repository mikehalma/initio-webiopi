webiopi().ready(function() {
    var sonarUp = webiopi().createButton("sonarUp", "Sonar Up", function() {
        webiopi().callMacro("sonarUp");
    });
    // $("#controls").append(sonarUp);

    setInterval(function() {
        webiopi().callMacro("irStatus", [], function(macro, args, response) {
            var status = JSON.parse(response);
            console.log('Status=' + status);
            if(status.left) {
                $('img.leftIrTrue').show();
                $('img.leftIrFalse').hide();
            } else {
                $('img.leftIrFalse').show();
                $('img.leftIrTrue').hide();
            }
            if(status.leftLine) {
                $('img.leftLineTrue').show();
                $('img.leftLineFalse').hide();
            } else {
                $('img.leftLineFalse').show();
                $('img.leftLineTrue').hide();
            }
            if(status.right) {
                $('img.rightIrTrue').show();
                $('img.rightIrFalse').hide();
            } else {
                $('img.rightIrFalse').show();
                $('img.rightIrTrue').hide();
            }
            if(status.rightLine) {
                $('img.rightLineTrue').show();
                $('img.rightLineFalse').hide();
            } else {
                $('img.rightLineFalse').show();
                $('img.rightLineTrue').hide();
            }
        });
    }, 1000);
    setIrImgSize('leftIr');
    setIrImgSize('rightIr');
    setIrImgSize('leftLine');
    setIrImgSize('rightLine');

    var forwardLeft = webiopi().createButton("forwardLeft", "", function() {
        webiopi().callMacro("forwardLeft");
    });
    $("#row1").append(forwardLeft);
    setImg('forwardLeft', 'forward-left.png');

    var forward = webiopi().createButton("forward", "", function() {
        webiopi().callMacro("forward");
    });
    $("#row1").append(forward);
    setImg('forward', 'forward.png');

    var forwardRight = webiopi().createButton("forwardRight", "", function() {
        webiopi().callMacro("forwardRight");
    });
    $("#row1").append(forwardRight);
    setImg('forwardRight', 'forward-right.png');

    var spinLeft = webiopi().createButton("spinLeft", "", function() {
        webiopi().callMacro("spinLeft");
    });
    $("#row2").append(spinLeft);
    setImg('spinLeft', 'spin-left.png');

    var stop = webiopi().createButton("stop", "", function() {
        webiopi().callMacro("stop");
    });
    $("#row2").append(stop);
    setImg('stop', 'stop.png');

    var spinRight = webiopi().createButton("spinRight", "", function() {
        webiopi().callMacro("spinRight");
    });
    $("#row2").append(spinRight);
    setImg('spinRight', 'spin-right.png');

    var reverseLeft = webiopi().createButton("reverseLeft", "", function() {
        webiopi().callMacro("reverseLeft");
    });
    $("#row3").append(reverseLeft);
    setImg('reverseLeft', 'reverse-left.png');

    var reverse = webiopi().createButton("reverse", "", function() {
        webiopi().callMacro("reverse");
    });
    $("#row3").append(reverse);
    setImg('reverse', 'reverse.png');

    var reverseRight = webiopi().createButton("reverseRight", "", function() {
        webiopi().callMacro("reverseRight");
    });
    $("#row3").append(reverseRight);
    setImg('reverseRight', 'reverse-right.png');

    // webiopi().refreshGPIO(true);
});

function setImg(buttonId, imgSrc) {
    var $button = $('#' + buttonId);
    $button.addClass('col-3');
    var getSize = function() {
        var h = $button.height();
        var w = $button.width();
        return Math.min(h, w);
    }
    var size = getSize();
    $button.append("<img src='img/" + imgSrc + "' height='" + size + "' width='" + size + "' />");
    var $img = $button.find('img');
    $(window).resize(function() {
        var size = getSize();
        $img.height(size);
        $img.width(size);
    });
    
}

function setIrImgSize(irDivId) {

    getContainerSize = function($container) {
        var h = $container.height();
        var w = $container.width();
        return Math.min(h, w);
    }
    var $div = $('#' + irDivId);
    var divSize = getContainerSize($div.closest('div.row')) - 20;
    $div.find('img').height(divSize).width(divSize);
    $(window).resize(function() {
        var size = getContainerSize($div);
        $div.find('img').height(size).width(size);
    });
}
