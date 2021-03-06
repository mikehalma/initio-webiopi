webiopi().ready(function() {

    var robot = {};
    robot.moving = false;
    irSensors.init(robot);
    buttons.init(robot);
    return;

});

/*
 * Create the buttons to control the robot and attach them to the screen
 */
var buttons = (function() {
    var self = {};

    self.init = function(robot) {
        self.robot = robot;
        createButtons();

    };


    var createButtons = function() {

        self.forwardLeft = new Btn.init({id: 'forwardLeft', rowId: 'row1', img: 'forward-left.png'});
        self.forward = new Btn.init({id: 'forward', rowId: 'row1', img: 'forward.png'});
        self.forwardRight = new Btn.init({id: 'forwardRight', rowId: 'row1', img: 'forward-right.png'});

        self.spinLeft = new Btn.init({id: 'spinLeft', rowId: 'row2', img: 'spin-left.png'});
        self.stop = new Btn.init({id: 'stop', rowId: 'row2', img: 'stop.png'});
        self.spinRight = new Btn.init({id: 'spinRight', rowId: 'row2', img: 'spin-right.png'});

        self.reverseLeft = new Btn.init({id: 'reverseLeft', rowId: 'row3', img: 'reverse-left.png'});
        self.reverse = new Btn.init({id: 'reverse', rowId: 'row3', img: 'reverse.png'});
        self.reverseRight = new Btn.init({id: 'reverseRight', rowId: 'row3', img: 'reverse-right.png'});

        $('#controls').on('click', 'button', function() {
            var button = $(this).attr('id');
            if(button == 'stop') {
                self.robot.moving = false;
            } else {
                self.robot.moving = true;
            }
        });
        
    };

    return self;
})();

/*
 * Create an instance of a button to control some aspect of the robot.
 * The button should be created with the function init, which expects 
 * the options:
 *      id - the id of the button to create
 *      rowId - the id of the row to attach the button to
 *      img - the name of the image to use on the button (relative to the img directory)
 */
var Btn = (function() {
    var pub = {};

    pub.init = function(options) {
        // Default the macro to be the same as the button id
        if(!options.macroName) {
            options.macroName = options.id;
        }
        pub.options = options;

        // The jQuery wrapped button as displayed
        pub.$button = webiopi().createButton(options.id, "", function() {
            webiopi().callMacro(options.macroName);
        });

        // Add the button to the screen and configure it
        var $row = $('#'+options.rowId);
        $row.append(pub.$button);
        var $img = setImg(pub.$button, options.img);
        setPressable(pub.$button);

    }

    /*
     * Assign the passed button with the passed image
     */
    var setImg = function($button, imgSrc) {
        $button.addClass('col-3');
        var imgSize = utils.getMinContainerDim($button);
        $button.append("<img src='img/" + imgSrc + "' height='" + imgSize + "' width='" + imgSize + "' />");
        var $img = $button.find('img');
        $(window).resize(function() {
            var size = utils.getMinContainerDim($button);
            $img.height(size);
            $img.width(size);
        });
        return $img;
    }

    /*
     * Make the button appear to be pressed
     */
    var setPressable = function($button) {
        $button.mousedown(function() {
            $('button.pressed').removeClass('pressed');
            $button.addClass('pressed');
        });
    };

    return pub;
})();

/*
 * The handler for the IR sensors display
 */
var irSensors = (function() {
    var self = {};
    self.imgs = {};

    self.init = function(robot) {
        self.robot = robot;
        self.imgs.$leftIrTrue = $('img#leftIrTrue');
        self.imgs.$leftIrFalse = $('img#leftIrFalse');
        self.imgs.$rightIrTrue = $('img#rightIrTrue');
        self.imgs.$rightIrFalse= $('img#rightIrFalse');
        self.imgs.$leftLineTrue = $('img#leftLineTrue');
        self.imgs.$leftLineFalse = $('img#leftLineFalse');
        self.imgs.$rightLineTrue = $('img#rightLineTrue');
        self.imgs.$rightLineFalse = $('img#rightLineFalse');

        setImgSizes();
        pollStatus(true);
        setInterval(pollStatus, 1000);
    };
    
    /*
     * Get the status of the IR sensors from the server.
     * The parameter stationary=true tells us to force the request even if 
     * the robot is not moving (normally we would stop checking the status
     * if the robot is stationary as the sensors should not change)
     */
    var pollStatus = function(stationary) {
        var pollIfStationary = false;
        if(stationary) {
            pollIfStationary = true;
        }
        // Do not check the status for a stationary robot unless we have specifically been asked to
        if(self.robot.moving != true && pollIfStationary == false) {
            return;
        }
        webiopi().callMacro("irStatus", [], function(macro, args, response) {
            var status = JSON.parse(response);
            if(status.left) {
                self.imgs.$leftIrTrue.show();
                self.imgs.$leftIrFalse.hide();
            } else {
                self.imgs.$leftIrTrue.hide();
                self.imgs.$leftIrFalse.show();
            }
            if(status.leftLine) {
                self.imgs.$leftLineTrue.show();
                self.imgs.$leftLineFalse.hide();
            } else {
                self.imgs.$leftLineTrue.hide();
                self.imgs.$leftLineFalse.show();
            }
            if(status.right) {
                self.imgs.$rightIrTrue.show();
                self.imgs.$rightIrFalse.hide();
            } else {
                self.imgs.$rightIrTrue.hide();
                self.imgs.$rightIrFalse.show();
            }
            if(status.rightLine) {
                self.imgs.$rightLineTrue.show();
                self.imgs.$rightLineFalse.hide();
            } else {
                self.imgs.$rightLineTrue.hide();
                self.imgs.$rightLineFalse.show();
            }
        });
    };

    var setImgSizes = function() {
        for(img in self.imgs) {
            if(!self.imgs.hasOwnProperty(img)) {
                continue;
            }
            var $img = self.imgs[img];
            var $div = $img.closest('div');
            setImgSize($div, $img);
            $img.hide();
        }
    };
    var setImgSize = function($div, $img) {
        var imgSize = utils.getMinContainerDim($div);
        $img.height(imgSize).width(imgSize);
        $(window).resize(function() {
            var size = utils.getMinContainerDim($div);
            $img.height(size).width(size);
        });
    };


    return self;
})();

var utils = (function() {
    var self = {};

    /*
     * Get the minimum height/width of the passed container
     */
    self.getMinContainerDim = function($container) {
        var h = $container.height();
        var w = $container.width();
        return Math.min(h, w);
    };

    return self;
})();
