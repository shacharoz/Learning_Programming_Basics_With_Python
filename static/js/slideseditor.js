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
var Preview = /** @class */ (function () {
    function Preview(src) {
        this.src = src;
    }
    Preview.prototype.open = function () {
        var containerPrimary = document.getElementsByClassName('container-primary')[0];
        var preview = document.createElement('div');
        preview.setAttribute('id', 'preview');
        var img = document.createElement('img');
        var btn = document.createElement('button');
        img.setAttribute('src', this.src);
        btn.innerText = '×';
        btn.onclick = (function (preview) {
            return preview.close;
        })(this);
        preview.addEventListener('click', (function (preview, btn, img) {
            return function (event) {
                if (img !== event.target && btn !== event.target) {
                    preview.close();
                }
            };
        })(this, btn, img));
        preview.appendChild(btn);
        preview.appendChild(img);
        containerPrimary.appendChild(preview);
    };
    Preview.prototype.close = function () {
        var containerPrimary = document.getElementsByClassName('container-primary')[0];
        var preview = document.getElementById('preview');
        containerPrimary.removeChild(preview);
    };
    return Preview;
}());
var SlidesEditor = /** @class */ (function () {
    /**
     *
     * @param slides The slides on which the editor should start.
     */
    function SlidesEditor(slides, images) {
        this.slides = slides;
        this.images = images;
    }
    /**
     *
     */
    SlidesEditor.prototype.populate = function () {
        var _this = this;
        var containerPrimary = document.getElementsByClassName('container-primary')[0];
        var slidesElement = document.getElementById('slides');
        if (document.getElementById('update')) {
            containerPrimary.removeChild(document.getElementById('update'));
        }
        if (slidesElement) {
            containerPrimary.removeChild(slidesElement);
        }
        if (document.getElementById('add')) {
            containerPrimary.removeChild(document.getElementById('add'));
        }
        if (document.getElementById('delete')) {
            containerPrimary.removeChild(document.getElementById('delete'));
        }
        if (document.getElementById('upload-container')) {
            containerPrimary.removeChild(document.getElementById('upload-container'));
        }
        slidesElement = document.createElement('div');
        slidesElement.setAttribute('id', 'slides');
        slidesElement.classList.add('row');
        containerPrimary.appendChild(slidesElement);
        this.slides.forEach(function (slide, index) {
            var slideCol = document.createElement('div');
            slideCol.classList.add('col-md-4', 'slide');
            slideCol.setAttribute('id', 'slide_' + String(index));
            slideCol.draggable = true;
            slideCol.ondragover = function (event) {
                event.preventDefault();
            };
            slideCol.ondragstart = (function (editor, index) {
                return function (event) {
                    event.dataTransfer.setData('index', String(index));
                };
            })(_this, index);
            slideCol.ondrop = (function (editor, index1) {
                return function (event) {
                    event.preventDefault();
                    var index2 = parseInt(event.dataTransfer.getData('index'));
                    editor.drop(index, index2);
                };
            })(_this, index);
            var slideContent = document.createElement('div');
            slideContent.classList.add('card', 'mb-4', 'shadow-sm');
            slideCol.appendChild(slideContent);
            var cardBody = document.createElement('div');
            cardBody.classList.add('card-body');
            slideCol.appendChild(cardBody);
            var heading = document.createElement('h3');
            heading.classList.add('text-center');
            heading.innerText = 'Slide ' + String(index + 1);
            cardBody.appendChild(heading);
            var titleControl = document.createElement('input');
            titleControl.setAttribute('id', 'title_' + String(index));
            titleControl.setAttribute('name', titleControl.getAttribute('id'));
            titleControl.setAttribute('type', 'text');
            titleControl.setAttribute('value', slide.title);
            titleControl.classList.add('form-control');
            cardBody.appendChild(titleControl);
            var imageControl = document.createElement('select');
            imageControl.setAttribute('id', 'image_' + String(index));
            imageControl.setAttribute('name', imageControl.getAttribute('id'));
            var imageOption = document.createElement('option');
            imageOption.setAttribute('value', '');
            imageOption.style.display = 'none';
            imageControl.appendChild(imageOption);
            _this.images.forEach(function (image) {
                var imageOption = document.createElement('option');
                imageOption.setAttribute('value', image);
                imageOption.innerText = image;
                if (slide.image === image) {
                    imageOption.selected = true;
                }
                imageControl.appendChild(imageOption);
            });
            imageControl.classList.add('form-control');
            cardBody.appendChild(imageControl);
            var timeControl = document.createElement('input');
            timeControl.setAttribute('id', 'time_' + String(index));
            timeControl.setAttribute('name', timeControl.getAttribute('id'));
            timeControl.setAttribute('type', 'text');
            timeControl.setAttribute('value', slide.time);
            timeControl.classList.add('form-control');
            cardBody.appendChild(timeControl);
            var previewBtn = document.createElement('button');
            previewBtn.classList.add('preview');
            var previewImg = document.createElement('img');
            previewImg.setAttribute('id', 'preview_' + String(index));
            previewImg.setAttribute('src', '/static/img/' + slide.image);
            previewImg.classList.add('img', 'fit');
            previewBtn.appendChild(previewImg);
            previewBtn.onclick = (function (src) {
                return function () {
                    var preview = new Preview(src);
                    preview.open();
                };
            })(previewImg.src);
            cardBody.appendChild(previewBtn);
            titleControl.addEventListener('input', (function (editor, index) {
                return function (event) {
                    var slide = editor.slides[index];
                    slide.title = event.target.value;
                    editor.repopulate(slide, index);
                };
            })(_this, index));
            imageControl.addEventListener('change', (function (editor, index) {
                return function (event) {
                    var slide = editor.slides[index];
                    slide.image = event.target.value;
                    editor.repopulate(slide, index);
                };
            })(_this, index));
            timeControl.addEventListener('input', (function (editor, index) {
                return function (event) {
                    var slide = editor.slides[index];
                    slide.time = event.target.value;
                    editor.repopulate(slide, index);
                };
            })(_this, index));
            slideContent.appendChild(cardBody);
            slideCol.appendChild(slideContent);
            slidesElement.appendChild(slideCol);
        });
        var addSlideBtn = document.createElement('button');
        addSlideBtn.classList.add('btn', 'btn-outline-success', 'shadow-sm');
        addSlideBtn.setAttribute('id', 'add');
        addSlideBtn.onclick = (function (editor) {
            return function (event) {
                editor.clone(-1);
            };
        })(this);
        addSlideBtn.ondragover = (function (addSlideBtn) {
            return function (event) {
                event.preventDefault();
                addSlideBtn.style.backgroundColor = '#28a745';
                addSlideBtn.style.color = '#fff';
            };
        })(addSlideBtn);
        addSlideBtn.ondragleave = (function (addSlideBtn) {
            return function () {
                addSlideBtn.style.backgroundColor = '#fff';
                addSlideBtn.style.color = '#28a745';
            };
        })(addSlideBtn);
        addSlideBtn.ondrop = (function (editor, addSlideBtn) {
            return function (event) {
                addSlideBtn.style.backgroundColor = '#fff';
                addSlideBtn.style.color = '#28a745';
                var index = parseInt(event.dataTransfer.getData('index'));
                editor.clone(index);
            };
        })(this, addSlideBtn);
        addSlideBtn.innerHTML = '+';
        containerPrimary.appendChild(addSlideBtn);
        var deleteBtn = document.createElement('div');
        deleteBtn.classList.add('btn', 'btn-outline-danger', 'shadow-sm');
        deleteBtn.setAttribute('id', 'delete');
        deleteBtn.ondragover = (function (deleteBtn) {
            return function (event) {
                event.preventDefault();
                var paths = deleteBtn.getElementsByTagName('path');
                for (var i = 0; i < paths.length; i++) {
                    var path = paths[i];
                    path.style.fill = '#fff';
                    deleteBtn.style.backgroundColor = '#dc3545';
                }
            };
        })(deleteBtn);
        deleteBtn.ondragleave = (function (deleteBtn) {
            return function () {
                var paths = deleteBtn.getElementsByTagName('path');
                for (var i = 0; i < paths.length; i++) {
                    var path = paths[i];
                    path.style.fill = '#dc3545';
                    deleteBtn.style.backgroundColor = '#fff';
                }
            };
        })(deleteBtn);
        deleteBtn.ondrop = (function (editor, deleteBtn) {
            return function (event) {
                var paths = deleteBtn.getElementsByTagName('path');
                for (var i = 0; i < paths.length; i++) {
                    var path = paths[i];
                    path.style.fill = '#dc3545';
                    deleteBtn.style.backgroundColor = '#fff';
                }
                var index = parseInt(event.dataTransfer.getData('index'));
                editor["delete"](index);
            };
        })(this, deleteBtn);
        deleteBtn.innerHTML = '<svg viewBox="0 0 26 26" version="1.1" width="5rem"><path stroke-width="2.0803" stroke-miterlimit="10" d="M9,4.429V3c0-1.421,0.619-2,2-2h4  c1.381,0,2,0.579,2,2v1.429"/><path d="M23,4L23,4c0-0.551-0.449-1-1-1H4C3.449,3,3,3.449,3,4l0,0H2v2h22V4H23z"/><path d="M4,7v16c0,1.654,1.346,3,3,3h12c1.654,0,3-1.346,3-3V7H4z M10,22H8V10h2V22z M14,22h-2V10h2V22z M18,22h-2  V10h2V22z"></svg>';
        containerPrimary.appendChild(deleteBtn);
        var updateBtn = document.createElement('button');
        updateBtn.setAttribute('id', 'update');
        updateBtn.onclick = (function (editor) {
            return function (event) {
                editor.update();
            };
        })(this);
        updateBtn.innerText = 'Update';
        updateBtn.classList.add('btn', 'btn-lg', 'btn-primary');
        containerPrimary.appendChild(updateBtn);
    };
    SlidesEditor.prototype.repopulate = function (slide, index) {
        this.slides[index] = slide;
        var slideElement = document.getElementById('slide_' + String(index));
        slideElement.ondragstart = (function (index) {
            return function (event) {
                event.dataTransfer.setData('index', index);
            };
        })(index);
        slideElement.ondrop = (function (editor, index1) {
            return function (event) {
                event.preventDefault();
                var index2 = event.dataTransfer.getData('index');
                editor.drop(index, index2);
            };
        })(this, index);
        var previewBtn = document.getElementsByClassName('preview')[index];
        var previewImg = document.getElementById('preview_' + String(index));
        previewImg.setAttribute('src', '/static/img/' + slide.image);
        previewBtn.onclick = (function (src) {
            return function () {
                new Preview(src).open();
            };
        })(previewImg.src);
        var updateBtn = document.getElementById('update');
        updateBtn.onclick = (function (editor) {
            return function (event) {
                editor.update();
            };
        })(this);
    };
    SlidesEditor.prototype.update = function () {
        return __awaiter(this, void 0, void 0, function () {
            var conn, btn, payload;
            return __generator(this, function (_a) {
                conn = new XMLHttpRequest();
                btn = document.getElementById('update');
                btn.innerText = 'Updating...';
                btn.disabled = true;
                conn.onload = (function (btn) {
                    return function () {
                        setTimeout(function () {
                            btn.innerText = 'Update';
                            btn.disabled = false;
                        }, 200);
                    };
                })(btn);
                payload = JSON.stringify(this.slides);
                conn.open('POST', '/slideshow/edit');
                conn.setRequestHeader('Content-Type', 'application/json');
                conn.send(payload);
                return [2 /*return*/];
            });
        });
    };
    SlidesEditor.prototype.drop = function (index1, index2) {
        var tmp = this.slides[index1];
        this.slides[index1] = this.slides[index2];
        this.slides[index2] = tmp;
        this.populate();
    };
    SlidesEditor.prototype.clone = function (index) {
        if (index === -1) {
            this.slides.push({ title: 'Edit Title', image: 'missing.png', time: '00:00' });
        }
        else {
            this.slides.push(this.slides[index]);
        }
        this.populate();
    };
    SlidesEditor.prototype["delete"] = function (index) {
        this.slides.splice(index, 1);
        this.populate();
    };
    return SlidesEditor;
}());
