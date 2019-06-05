interface Slide {
  title: string;
  image: string;
  time: string;
}


class Preview {

  private isOpen: boolean;
  private src: string;

  constructor (src: string) {
    this.src = src;
  }

  public open() {
    let containerPrimary = document.getElementsByClassName('container-primary')[0];
    let preview = document.createElement('div');
    preview.setAttribute('id', 'preview');
    let img = document.createElement('img');
    let btn = document.createElement('button');
    img.setAttribute('src', this.src);
    preview.addEventListener('click', ((preview: Preview, img: HTMLImageElement) => {
      return (event: MouseEvent) => {
        if (img !== event.target) {
          preview.close();
        }
      };
    })(this, img));
    preview.appendChild(img);
    containerPrimary.appendChild(preview);
  }

  public close() {
    let containerPrimary = document.getElementsByClassName('container-primary')[0];
    let preview = document.getElementById('preview');
    containerPrimary.removeChild(preview);
  }
}


class SlidesEditor {

  private slides: Slide[];
  private images: string[];

  /**
   * 
   * @param slides The slides on which the editor should start.
   */
  constructor (slides: Slide[], images: string[]) {
    this.slides = slides;
    this.images = images;
  }

  /**
   * 
   */
  public populate() {
    const containerPrimary = document.getElementsByClassName('container-primary')[0];
    let slidesElement = document.getElementById('slides');

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

    this.slides.forEach((slide, index) => {

      let slideCol = document.createElement('div');
      slideCol.classList.add('col-md-4', 'slide');
      slideCol.setAttribute('id', 'slide_' + String(index));
      slideCol.draggable = true;
      slideCol.ondragover = event => {
        event.preventDefault()
      };
      slideCol.ondragstart = ((editor: SlidesEditor, index: number) => {
        return (event: DragEvent) => {
          event.dataTransfer.setData('index', String(index));
        };
      })(this, index);
      slideCol.ondrop = ((editor: SlidesEditor, index1: number) => {
        return (event: DragEvent) => {
          event.preventDefault();
          let index2 = parseInt(event.dataTransfer.getData('index'));
          editor.drop(index, index2);
        };
      })(this, index);

      let slideContent = document.createElement('div');
      slideContent.classList.add('card', 'mb-4', 'shadow-sm');
      slideCol.appendChild(slideContent);

      let cardBody = document.createElement('div');
      cardBody.classList.add('card-body');
      slideCol.appendChild(cardBody);

      let heading = document.createElement('h3');
      heading.classList.add('text-center');
      heading.innerText = 'Slide ' + String(index + 1);
      cardBody.appendChild(heading);

      let titleControl = document.createElement('input');
      titleControl.setAttribute('id', 'title_' + String(index));
      titleControl.setAttribute('name', titleControl.getAttribute('id'));
      titleControl.setAttribute('type', 'text');
      titleControl.setAttribute('value', slide.title);
      titleControl.classList.add('form-control');
      titleControl.addEventListener('mousedown', ((parent: HTMLElement) => {
        return () => {
          parent.draggable = false;
        };
      })(slideCol));
      titleControl.addEventListener('mouseup', ((parent: HTMLElement) => {
        return () => {
          parent.draggable = true;
        };
      })(slideCol));
      cardBody.appendChild(titleControl);

      let imageControl = document.createElement('select');
      imageControl.setAttribute('id', 'image_' + String(index));
      imageControl.setAttribute('name', imageControl.getAttribute('id'));

      let imageOption = document.createElement('option');
      imageOption.setAttribute('value', '');
      imageOption.style.display = 'none';
      imageControl.appendChild(imageOption);
      
      this.images.forEach(image => {
        let imageOption = document.createElement('option');
        const imgParts = image.split('/');
        const imageName = imgParts[imgParts.length - 1];
        imageOption.setAttribute('value', image);
        imageOption.innerText = imageName;
        if (slide.image === image) {
          imageOption.selected = true;
        }
        imageControl.appendChild(imageOption);
      });

      imageControl.classList.add('form-control', 'inline');
      imageControl.addEventListener('mousedown', ((parent: HTMLElement) => {
        return () => {
          parent.draggable = false;
        };
      })(slideCol));
      imageControl.addEventListener('mouseup', ((parent: HTMLElement) => {
        return () => {
          parent.draggable = true;
        };
      })(slideCol));
      cardBody.appendChild(imageControl);

      let uploadBtn = document.createElement('button');
      uploadBtn.innerText = 'Upload';
      uploadBtn.classList.add('btn', 'btn-primary', 'form-btn');
      uploadBtn.onclick = ((editor: SlidesEditor, index: number) => {
        return () => {
          let uploadControl = document.createElement('input');
          uploadControl.setAttribute('type', 'file');
          uploadControl.setAttribute('accept', 'image/*');
          uploadControl.addEventListener('input', ((editor: SlidesEditor, index: number) => {
            return (event: Event) => {
              const file = (<HTMLInputElement> event.target).files[0];
              editor.upload(file, index);
            };
          })(editor, index));
          uploadControl.click();
        };
      })(this, index);
      uploadBtn.addEventListener('mousedown', ((parent: HTMLElement) => {
        return () => {
          parent.draggable = false;
        };
      })(slideCol));
      uploadBtn.addEventListener('mouseup', ((parent: HTMLElement) => {
        return () => {
          parent.draggable = true;
        };
      })(slideCol));
      cardBody.appendChild(uploadBtn);

      let timeControl = document.createElement('input');
      timeControl.setAttribute('id', 'time_' + String(index));
      timeControl.setAttribute('name', timeControl.getAttribute('id'));
      timeControl.setAttribute('type', 'text');
      timeControl.setAttribute('value', slide.time);
      timeControl.classList.add('form-control');
      timeControl.addEventListener('mousedown', ((parent: HTMLElement) => {
        return () => {
          parent.draggable = false;
        };
      })(slideCol));
      timeControl.addEventListener('mouseup', ((parent: HTMLElement) => {
        return () => {
          parent.draggable = true;
        };
      })(slideCol));
      cardBody.appendChild(timeControl);

      let previewBtn = document.createElement('button');
      previewBtn.classList.add('preview');
      let previewImg = document.createElement('img');
      previewImg.setAttribute('id', 'preview_' + String(index));
      previewImg.setAttribute('src', slide.image);
      previewImg.classList.add('img', 'fit');
      previewBtn.appendChild(previewImg);
      previewBtn.onclick = ((src: string) => {
        return () => {
          let preview = new Preview(src);
          preview.open();
        };
      })(previewImg.src);
      cardBody.appendChild(previewBtn);

      titleControl.addEventListener('input', ((editor: SlidesEditor, index: number) => {
        return (event) => {
          const slide = editor.slides[index];
          slide.title = event.target.value;
          editor.repopulate(slide, index);
        };
      })(this, index));

      imageControl.addEventListener('change', ((editor: SlidesEditor, index: number) => {
        return (event: Event) => {
          const slide = editor.slides[index];
          slide.image = (<HTMLSelectElement> event.target).value;
          editor.repopulate(slide, index);
        };
      })(this, index));

      timeControl.addEventListener('input', ((editor: SlidesEditor, index: number) => {
        return (event) => {
          const slide = editor.slides[index];
          slide.time = event.target.value;
          editor.repopulate(slide, index);
        };
      })(this, index));

      slideContent.appendChild(cardBody);
      slideCol.appendChild(slideContent);
      slidesElement.appendChild(slideCol);
    });

    let addSlideBtn = document.createElement('button');
    addSlideBtn.classList.add('btn', 'btn-outline-success', 'shadow-sm');
    addSlideBtn.setAttribute('id', 'add');
    addSlideBtn.onclick = ((editor: SlidesEditor) => {
      return (event) => {
        editor.clone(-1);
      };
    })(this);
    addSlideBtn.ondragover = ((addSlideBtn: HTMLElement) => {
      return (event: DragEvent) => {
        event.preventDefault();
        addSlideBtn.style.backgroundColor = '#28a745';
        addSlideBtn.style.color = '#fff';
      };
    })(addSlideBtn);
    addSlideBtn.ondragleave = ((addSlideBtn: HTMLElement) => {
      return () => {
        addSlideBtn.style.backgroundColor = '#fff';
        addSlideBtn.style.color = '#28a745';
      };
    })(addSlideBtn);
    addSlideBtn.ondrop = ((editor: SlidesEditor, addSlideBtn: HTMLElement) => {
      return (event: DragEvent) => {
        addSlideBtn.style.backgroundColor = '#fff';
        addSlideBtn.style.color = '#28a745';
        const index = parseInt(event.dataTransfer.getData('index'));
        editor.clone(index);
      };
    })(this, addSlideBtn);
    addSlideBtn.innerHTML = '+';
    containerPrimary.appendChild(addSlideBtn);

    let deleteBtn = document.createElement('div');
    deleteBtn.classList.add('btn', 'btn-outline-danger', 'shadow-sm');
    deleteBtn.setAttribute('id', 'delete');
    deleteBtn.ondragover = ((deleteBtn: HTMLElement) => {
      return (event: DragEvent) => {
        event.preventDefault();
        const paths = deleteBtn.getElementsByTagName('path');
        for (let i = 0; i < paths.length; i++) {
          const path = paths[i];
          path.style.fill = '#fff';
          deleteBtn.style.backgroundColor = '#dc3545';
        }
      };
    })(deleteBtn);
    deleteBtn.ondragleave = ((deleteBtn: HTMLElement) => {
      return () => {
        const paths = deleteBtn.getElementsByTagName('path');
        for (let i = 0; i < paths.length; i++) {
          const path = paths[i];
          path.style.fill = '#dc3545';
          deleteBtn.style.backgroundColor = '#fff';
        }
      };
    })(deleteBtn);
    deleteBtn.ondrop = ((editor: SlidesEditor, deleteBtn: HTMLElement) => {
      return (event: DragEvent) => {
        const paths = deleteBtn.getElementsByTagName('path');
        for (let i = 0; i < paths.length; i++) {
          const path = paths[i];
          path.style.fill = '#dc3545';
          deleteBtn.style.backgroundColor = '#fff';
        }
        const index = parseInt(event.dataTransfer.getData('index'));
        editor.delete(index);
      };
    })(this, deleteBtn);
    deleteBtn.innerHTML = '<svg viewBox="0 0 26 26" version="1.1" width="5rem"><path stroke-width="2.0803" stroke-miterlimit="10" d="M9,4.429V3c0-1.421,0.619-2,2-2h4  c1.381,0,2,0.579,2,2v1.429"/><path d="M23,4L23,4c0-0.551-0.449-1-1-1H4C3.449,3,3,3.449,3,4l0,0H2v2h22V4H23z"/><path d="M4,7v16c0,1.654,1.346,3,3,3h12c1.654,0,3-1.346,3-3V7H4z M10,22H8V10h2V22z M14,22h-2V10h2V22z M18,22h-2  V10h2V22z"></svg>';
    containerPrimary.appendChild(deleteBtn);

    let updateBtn = document.createElement('button');
    updateBtn.setAttribute('id', 'update');
    updateBtn.onclick = ((editor: SlidesEditor) => {
      return (event) => {
        editor.update();
      };
    })(this);
    updateBtn.innerText = 'Update';
    updateBtn.classList.add('btn', 'btn-lg', 'btn-primary');

    containerPrimary.appendChild(updateBtn);
  }

  public repopulate(slide: Slide, index: number) {
    this.slides[index] = slide;
    const slideElement = document.getElementById('slide_' + String(index));
    slideElement.ondragstart = ((index: number) => {
      return (event) => {
        event.dataTransfer.setData('index', index);
      };
    })(index);
    slideElement.ondrop = ((editor: SlidesEditor, index1: number) => {
      return (event) => {
        event.preventDefault();
        let index2 = event.dataTransfer.getData('index');
        editor.drop(index, index2);
      };
    })(this, index);
    const previewBtn = <HTMLButtonElement> document.getElementsByClassName('preview')[index];
    const previewImg = <HTMLImageElement> document.getElementById('preview_' + String(index));
    previewImg.setAttribute('src', slide.image);
    previewBtn.onclick = ((src: string) => {
      return () => {
        new Preview(src).open();
      };
    })(previewImg.src);

    const updateBtn = <HTMLButtonElement> document.getElementById('update');
    updateBtn.onclick = ((editor: SlidesEditor) => {
      return (event) => {
        editor.update();
      };
    })(this);
  }

  public async update() {
    const conn = new XMLHttpRequest();

    let btn = <HTMLButtonElement> document.getElementById('update');
    btn.innerText = 'Updating...';
    btn.disabled = true;

    conn.onload = ((btn: HTMLButtonElement) => {
      return () => {
        setTimeout(() => {
          btn.innerText = 'Update';
          btn.disabled = false;
        }, 200);
      };
    })(btn);

    const payload = JSON.stringify(this.slides);

    conn.open('POST', window.location.href);
    conn.setRequestHeader('Content-Type', 'application/json');
    conn.send(payload);
  }

  public async upload(file: File, index: number) {
    const conn = new XMLHttpRequest();

    let loader = document.createElement('div');
    loader.classList.add('loader');
    document.body.appendChild(loader);

    conn.onload = ((editor: SlidesEditor, index: number, loader) => {
      return () => {
        const filename = '/static/users' + window.location.pathname.replace(new RegExp('(\/edit)$'), '') + '/' + file.name;
        if (editor.images.indexOf(filename) === -1) {
          editor.images.push(filename);
          editor.images.sort();
        }
        editor.slides[index].image = filename;
        editor.populate();
        document.body.removeChild(loader);
      };
    })(this, index, loader);

    const payload = new FormData();
    payload.append('image', file);

    conn.open('POST', window.location.href.replace(new RegExp('(\/edit)$'), '/upload'));
    conn.send(payload);
  }

  public drop(index1: number, index2: number) {
    let tmp = this.slides[index1];
    this.slides[index1] = this.slides[index2];
    this.slides[index2] = tmp;
    this.populate();
  }

  public clone(index: number) {
    if (index === -1) {
      this.slides.push({ title: 'Edit Title', image: '/static/img/default.png', time: '00:00' });
    } else {
      this.slides.push(this.slides[index]);
    }
    this.populate();
  }

  public delete(index: number) {
    this.slides.splice(index, 1);
    this.populate();
  }
}