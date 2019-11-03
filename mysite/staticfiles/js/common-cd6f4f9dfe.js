
var uri = window.location.pathname;

if (isTargetToRedirectMobilePage(uri)) {
	var redirectURL = 'https://m.cafe.daum.net';

	if (uri == "/_c21_/fancafe_list") {
		redirectURL = redirectURL + '/_fancafe';
	} else if (uri == "/_c21_/royalcafe") {
		redirectURL = redirectURL + '/_royalcafe';
	} else if (uri == "/_c21_/my_cafe") {
		redirectURL = redirectURL + '/_myCafe';
	} else if (uri == "/_c21_/my_news") {
		redirectURL = redirectURL + '/_myAlimis';
	} else if (uri == "/_c21_/my_bookmark") {
		redirectURL = redirectURL + '/_bookmarks';
	}
	document.location.replace(redirectURL);
}

function isTargetToRedirectMobilePage(uri) {
	return !(getCookie("M_P2M") || !checkMobileUserAgent() || uri.indexOf("/_c21_/mymsgbox_main") > -1);
}

function setCookie(name, value, expiredays, domain) {
	var exdate = new Date();
	exdate.setDate(exdate.getDate() + expiredays);
	if (typeof(domain) == 'undefined') {
		domain = document.location.hostname;
	}
	document.cookie = name + "=" + escape(value) + "; path=/; domain=" + domain + ((expiredays == null) ? "" : ";expires=" + exdate.toGMTString());
}

function getCookie(name) {
	if (document.cookie.length > 0) {
		var c_start = document.cookie.indexOf(name + "=");
		if (c_start != -1) {
			c_start = c_start + name.length + 1;
			var c_end = document.cookie.indexOf(";", c_start);
			if (c_end == -1) c_end = document.cookie.length;
			return unescape(document.cookie.substring(c_start, c_end));
		}
	}
	return "";
}

function deleteCookie(name, domain) {
	var expireDate = new Date();
	expireDate.setDate(expireDate.getDate() - 1);
	if (typeof(domain) == 'undefined') {
		domain = document.location.hostname;
	}
	document.cookie = name + "= " + "; path=/; domain=" + domain + "; expires=" + expireDate.toGMTString() + ";";
}

function checkMobileUserAgent() {
	var MobileDevice = [/lgtelecom/, /opera.*skt/, /ppc.*opera/, /smartphone.*opera/, /800*480;nate/, /nate.*browser/, /mobile safari/, /iriver/, /iemobile navi/, /polaris/, /iphone/, /dolfin/, /ipad/];
	var isMobile = false;
	for (var i = MobileDevice.length - 1; i >= 0; i--) {
		if (navigator.userAgent.toLowerCase().search(MobileDevice[i]) > -1) {
			isMobile = true;
			break;
		}
	}
	return isMobile;
}

function checkIE() {
	var ieua = [/msie/, /trident/];
	var isIE = false;
	for (var i = ieua.length - 1; i >= 0; i--) {
		if (navigator.userAgent.toLowerCase().search(ieua[i]) > -1) {
			isIE = true;
			break;
		}
	}
	return isIE;
}

jQuery(function(){

	var daumQ = jQuery("#q")
	var focusCounter = {
		count: 0,
		lastRetainObj: null,
		lastReleaseObj: null,
		isSearchMode: false,
		retain: function(lastRetainObj){
			if (lastRetainObj && this.lastRetainObj == lastRetainObj) {
				this.lastRetainObj = null;
				return;
			}
			this.lastRetainObj = lastRetainObj;
			this.count++;
		},
		release: function(lastReleaseObj){
			if (lastReleaseObj && this.lastReleaseObj == lastReleaseObj) {
				this.lastReleaseObj = null;
				return;
			}
			this.lastReleaseObj = lastReleaseObj;

			if(this.count > 0) {
				this.count--;
			} else {
				promiseHide();
			}
		},
		isFree: function(){
			return this.count < 1;
		},
		reset: function(){
			this.count = 0;
			this.lastRetainObj = null;
			this.lastReleaseObj = null;
		}
	};

	var focusTimer = null;
	var promiseHide = function(){
		clearTimeout(focusTimer);
		focusTimer = setTimeout(function(){
			if (focusCounter.isFree()){
				hideSearchOptionLayer();
			}
		}, 350);
	};

	var showSearchOptionLayer = function() {
		jQuery("#searchOptionLayer").show();
		jQuery('#selectedOption').attr('aria-expanded', true);
		jQuery("#daumSearchOption").addClass("opt_search opt_open");
		jQuery(".list_opt input[type=radio]:checked").focus().parent().addClass('on');
	};

	var hideSearchOptionLayer = function() {
		jQuery("#searchOptionLayer").css("display", "none");
		jQuery('#selectedOption').attr('aria-expanded', false);
		jQuery("#daumSearchOption").removeClass("opt_search opt_open").addClass("opt_search");
		focusCounter.reset();
	};

	var isSelectedOptionClickEvent = false;
	jQuery('#selectedOption').click(function(evt) {
		evt.preventDefault();
		isSelectedOptionClickEvent = !isSelectedOptionClickEvent;
		toggleSearchOption();
	});

	function toggleSearchOption() {
		if (!jQuery("#searchOptionLayer").is(':visible')) {
			showSearchOptionLayer();
		} else {
			hideSearchOptionLayer();
		}
	}

	daumQ.focus(function() {
		hideSearchOptionLayer();
		jQuery(".box_searchbar").addClass('search_on');
	}).blur(function() {
		jQuery(".box_searchbar").removeClass('search_on');
	});

	jQuery('#searchOptionLayer').find('.link_opt').on('click', function (e) {
		e.preventDefault();
		var option;
		var text;
		switch(e.target.id) {
			case 'radAll':
				option = '';
				text = '카페검색';
				break;
			case 'radDaumSearch':
				option = 'daumsearch';
				text = '통합검색';
				break;
			case 'radCafeName':
				option = 'name';
				text = '카페이름';
				break;
			case 'radCafeArticle':
				option = 'board';
				text = '카페글';
				break;
		}
		jQuery('#searchOption').val(option);
		$('#selectedOption').find('.selected_option_text').html(text);
		decideSelectSearchOption();
	});

	function decideSelectSearchOption() {
		hideSearchOptionLayer();
		daumQ.focus().select();
	}
	jQuery('#suggest_box').on('click', 'li', function () {
		jQuery('#daumSearch').submit();
	})

	new suggest.Suggest(jQuery('.search_cafe')[0], {
		inputEl: 'q',
		APIServer: {
			host: 'https://suggest.cafe.daum.net/suggest',
			queries: {
				'limit':'5'
			}
		},
		suggestBoxEl: 'suggest_box',
		suggestLimit: 5,
		autoFocus: 'WRITE'
	});
	jQuery('#daumSearch').on('submit', function(e) {
		e.preventDefault();
		if(!this.isSearchMode){
			this.isSearchMode = true;
			jQuery('#daumSearch').find('.search_choice').addClass('search_open');
			jQuery('#selectedOption').focus();
			jQuery('#daumSearch').find('.ico_search').text('검색하기');
			return false;
		}
		if(daumQ.val().trim() === '') {
			alert('검색어를 입력해주세요')
			daumQ.focus().select();
			return false;
		}
		var txt = jQuery("#selectedOption").find(".selected_option_text").text();

		if(txt === '통합검색'){
			var q = daumQ.val();
			window.open("http://search.daum.net/search?w=tot&DA=60A&q=" + q);
		} else {
			this.submit();
		}
	});
	jQuery('#link_top').on('click', function(){
		jQuery(window).scrollTop(0);
	});
	
	var $window = $(window);
	var $btnTop = $('#link_top .ico_top');
	var windowHeight = $window.innerHeight();
	$window.on('scroll', function() {
		$btnTop.addClass('active');
		if ($(window).scrollTop() < windowHeight) {
			$btnTop.removeClass('active');
		}
	});

	if(getCookie("M_P2M") && checkMobileUserAgent()){
		var redirectMobileBtn = jQuery("<div id='redirect_mobile'><a href=\"https://m.cafe.daum.net\" onclick=\"deleteCookie(\'M_P2M\',\'.daum.net\');\" class=\"btn_go_mobile\"><span>모바일화면 이동</span></a></div>");
		jQuery("body").append(redirectMobileBtn);
	}
	// ie conditional css
	if(checkIE()) {
		$('body').addClass('ie')
	}
});


$(window).on('load', function(){
	if(checkIE()) {
		$('#cSub').find('.snb_cafe .list_snb .link_snb').css('fontSize', '24px')
		$('#cSub').find('.wrap_inform .link_item').css('fontSize', '14px')
	}
});
