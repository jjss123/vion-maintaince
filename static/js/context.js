/* 
 * Context.js
 * Copyright Jacob Kelley
 * MIT License
 * Modified by hylide
 * Update Note:
 * 1. Reorgnized structure, use prototype-chains, for multi-instances,
 * 2. Add custom "data-*" attribute
 */

var relation = new Array(),
	count = 0;
function Context() {

	this.options = {
		fadeSpeed: 100,
		filter: function ($obj) {
			// Modify $obj, Do not return
		},
		above: 'auto',
		preventDoubleContext: false,
		compress: false
	};
}

Context.prototype.init = function (opts) {
	var options;
	this.options = $.extend({}, this.options, opts);
	options = this.options;

	$(document).on('click', 'html', function () {
		setTimeout(function () {
			$('.dropdown-context-active').fadeOut(options.fadeSpeed, function () {
				$('.dropdown-context-active').css({ display: '' }).find('.drop-left').removeClass('drop-left');
				// TODO: mi zhi kadun
				$('.dropdown-context-active').removeClass('dropdown-context-active');
			});
		}, 0);
	});
	if (options.preventDoubleContext) {
		$(document).on('contextmenu', '.dropdown-context', function (e) {
			e.preventDefault();
		});
	}
	$(document).on('mouseenter', '.dropdown-submenu', function () {
		var $sub = $(this).find('.dropdown-context-sub:first'),
			subWidth = $sub.width(),
			subLeft = $sub.offset().left,
			collision = (subWidth + subLeft) > window.innerWidth;
		if (collision) {
			$sub.addClass('drop-left');
		}
	});
}

Context.prototype.settings = function (opts) {
	this.options = $.extend({}, this.options, opts);
	this.count = 0;
}

Context.prototype.buildMenu = function (data, id, subMenu) {
	var subClass = (subMenu) ? ' dropdown-context-sub' : '',
		compressed = this.options.compress ? ' compressed-context' : '',
		$menu = $('<ul class="dropdown-menu dropdown-context' + subClass + compressed + '" id="dropdown-' + id + '"></ul>');
	var i = 0, linkTarget = '', custom_data = '';
	for (i; i < data.length; i++) {
		if (typeof data[i].divider !== 'undefined') {
			$menu.append('<li class="divider"></li>');
		} else if (typeof data[i].header !== 'undefined') {
			$menu.append('<li class="nav-header">' + data[i].header + '</li>');
		} else {
			if (typeof data[i].href == 'undefined') {
				data[i].href = '#';
			}
			if (typeof data[i].custom_data !== 'undefined') {
				custom_data = ' data-custom="' + count + '"';
				count++;
			}
			if (typeof data[i].target !== 'undefined') {
				linkTarget = ' target="' + data[i].target + '"';
			}
			if (typeof data[i].subMenu !== 'undefined') {
				$sub = ('<li class="dropdown-submenu"><a tabindex="-1" href="' + data[i].href + '">' + data[i].text + '</a></li>');
			} else {
				$sub = $('<li><a tabindex="-1" href="' + data[i].href + '"' + linkTarget + custom_data + '>' + data[i].text + '</a></li>');
			}
			if (typeof data[i].action !== 'undefined') {
				var actiond = new Date(),
					actionID = 'event-' + actiond.getTime() * Math.floor(Math.random() * 100000),
					eventAction = data[i].action;
				$sub.find('a').attr('id', actionID);
				$('#' + actionID).addClass('context-event');
				$(document).on('click', '#' + actionID, eventAction);
			}
			$menu.append($sub);
			if (typeof data[i].subMenu != 'undefined') {
				var subMenuData = this.buildMenu(data[i].subMenu, id, true);
				$menu.find('li:last').append(subMenuData);
			}
		}
		if (typeof this.options.filter == 'function') {
			this.options.filter($menu.find('li:last'));
		}
	}
	return $menu;
}

Context.prototype.attach = function (selector, data) {

	var d = new Date(),
		id = d.getTime(),
		$menu = this.buildMenu(data, id),
		options = this.options;
	relation[selector] = id;
	$('body').append($menu);


	$('#' + selector).on('contextmenu', function (e) {
		var drId = relation[this.getAttribute('id')]

		e.preventDefault();
		e.stopPropagation();

		$('.dropdown-context:not(.dropdown-context-sub)').hide();

		$dd = $('#dropdown-' + drId);
		$dd.addClass('dropdown-context-active');
		if (typeof options.above == 'boolean' && options.above) {
			$dd.addClass('dropdown-context-up').css({
				top: e.pageY - 20 - $('#dropdown-' + drId).height(),
				left: e.pageX - 13
			}).fadeIn(options.fadeSpeed);
		} else if (typeof options.above == 'string' && options.above == 'auto') {
			$dd.removeClass('dropdown-context-up');
			var autoH = $dd.height() + 12;
			if ((e.pageY + autoH) > $('html').height()) {
				$dd.addClass('dropdown-context-up').css({
					top: e.pageY - 20 - autoH,
					left: e.pageX - 13
				}).fadeIn(options.fadeSpeed);
			} else {
				$dd.css({
					top: e.pageY + 10,
					left: e.pageX - 13
				}).fadeIn(options.fadeSpeed);
			}
		}
	});
}

Context.prototype.destroy = function (selector) {
	$(selector).off('contextmenu').off('click', '.context-event');
}