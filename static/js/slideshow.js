var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : new P(function (resolve) { resolve(result.value); }).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
var __generator = (this && this.__generator) || function (thisArg, body) {
    var _ = { label: 0, sent: function() { if (t[0] & 1) throw t[1]; return t[1]; }, trys: [], ops: [] }, f, y, t, g;
    return g = { next: verb(0), "throw": verb(1), "return": verb(2) }, typeof Symbol === "function" && (g[Symbol.iterator] = function() { return this; }), g;
    function verb(n) { return function (v) { return step([n, v]); }; }
    function step(op) {
        if (f) throw new TypeError("Generator is already executing.");
        while (_) try {
            if (f = 1, y && (t = op[0] & 2 ? y["return"] : op[0] ? y["throw"] || ((t = y["return"]) && t.call(y), 0) : y.next) && !(t = t.call(y, op[1])).done) return t;
            if (y = 0, t) op = [op[0] & 2, t.value];
            switch (op[0]) {
                case 0: case 1: t = op; break;
                case 4: _.label++; return { value: op[1], done: false };
                case 5: _.label++; y = op[1]; op = [0]; continue;
                case 7: op = _.ops.pop(); _.trys.pop(); continue;
                default:
                    if (!(t = _.trys, t = t.length > 0 && t[t.length - 1]) && (op[0] === 6 || op[0] === 2)) { _ = 0; continue; }
                    if (op[0] === 3 && (!t || (op[1] > t[0] && op[1] < t[3]))) { _.label = op[1]; break; }
                    if (op[0] === 6 && _.label < t[1]) { _.label = t[1]; t = op; break; }
                    if (t && _.label < t[2]) { _.label = t[2]; _.ops.push(op); break; }
                    if (t[2]) _.ops.pop();
                    _.trys.pop(); continue;
            }
            op = body.call(thisArg, _);
        } catch (e) { op = [6, e]; y = 0; } finally { f = t = 0; }
        if (op[0] & 5) throw op[1]; return { value: op[0] ? op[1] : void 0, done: true };
    }
};
var SlideShow = /** @class */ (function () {
    function SlideShow(slides, index) {
        this.slides = slides;
        var tmpIndex = window.location.hash.split('#')[1];
        if (+tmpIndex === +tmpIndex) {
            var _index = parseInt(tmpIndex);
            if (this.slides[tmpIndex] !== undefined) {
                this.index = _index - 1;
            }
            else {
                this.index = index;
            }
        }
        else {
            this.index = index;
        }
        if (!(this.index in this.slides)) {
            this.index = 0;
        }
        this.slidesLoaded = 0;
        this.highest = this.index;
    }
    SlideShow.prototype.populate = function () {
        window.location.hash = '#' + String(this.index + 1);
        var slide = this.slides[this.index];
        if (this.index < this.slidesLoaded) {
            this.load(slide);
        }
        document.title = "Bologna 1980 - " + slide.title;
        var titleElement = document.getElementById('title');
        titleElement.innerText = slide.title;
        document.body.style.background = "url(\"" + slide.image + "\") no-repeat center center fixed";
        document.body.style.backgroundSize = 'cover';
        var timeElement = document.getElementById('time');
        timeElement.innerText = slide.time;
        var backBtn = document.getElementById('back');
        if (this.index === 0) {
            backBtn.style.display = 'none';
        }
        else {
            backBtn.style.display = 'block';
        }
        var nextBtn = document.getElementById('next');
        if (this.index === this.slides.length - 1) {
            nextBtn.style.display = 'none';
        }
        else {
            nextBtn.style.display = 'block';
        }
    };
    SlideShow.prototype.load = function (slide) {
        var img = document.createElement('img').setAttribute('src', slide.image);
        this.slidesLoaded++;
    };
    SlideShow.prototype.preload = function () {
        return __awaiter(this, void 0, void 0, function () {
            var slide;
            return __generator(this, function (_a) {
                while (this.slides.length > this.slidesLoaded) {
                    slide = this.slides[this.slidesLoaded];
                    this.load(slide);
                }
                return [2 /*return*/];
            });
        });
    };
    SlideShow.prototype.sync = function () {
        return __awaiter(this, void 0, void 0, function () {
            var conn, payload;
            return __generator(this, function (_a) {
                conn = new XMLHttpRequest();
                payload = JSON.stringify({ index: this.index });
                conn.open('POST', window.location.href);
                conn.setRequestHeader('Content-Type', 'application/json');
                conn.send(payload);
                return [2 /*return*/];
            });
        });
    };
    SlideShow.prototype.back = function () {
        this.index--;
        this.populate();
    };
    SlideShow.prototype.next = function () {
        this.index++;
        this.populate();
        if (this.index > this.highest) {
            this.sync();
        }
    };
    return SlideShow;
}());
