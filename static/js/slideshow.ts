interface Slide {
  title: string;
  image: string;
  time: string;
}

class SlideShow {

  private index: number;
  private slides: Slide[];
  private slidesLoaded: number;
  private highest: number;

  constructor (slides: Slide[], index: number) {
    this.slides = slides;
    let tmpIndex = window.location.hash.split('#')[1];
    if (+tmpIndex === +tmpIndex) {
      let _index = parseInt(tmpIndex);
      if (this.slides[tmpIndex] !== undefined) {
        this.index = _index - 1;
      } else {
        this.index = index;
      }
    } else {
      this.index = index;
    }
    if (!(this.index in this.slides)) {
      this.index = 0;
    }
    this.slidesLoaded = 0;
    this.highest = this.index;
  }

  public populate(): void {
    window.location.hash = '#' + String(this.index + 1);
    const slide = this.slides[this.index];
    if (this.index < this.slidesLoaded) {
      this.load(slide);
    }
    document.title = `Bologna 1980 - ${slide.title}`;
    const titleElement = document.getElementById('title');
    titleElement.innerText = slide.title;
    document.body.style.background = `url("${slide.image}") no-repeat center center fixed`;
    document.body.style.backgroundSize = 'cover';
    const timeElement = document.getElementById('time');
    timeElement.innerText = slide.time;
    const backBtn = document.getElementById('back');
    if (this.index === 0) {
      backBtn.style.display = 'none';
    } else {
      backBtn.style.display = 'block';
    }
    const nextBtn = document.getElementById('next');
    if (this.index === this.slides.length - 1) {
      nextBtn.style.display = 'none';
    } else {
      nextBtn.style.display = 'block';
    }
  }

  public load(slide: Slide): void {
    const img = document.createElement('img').setAttribute('src', slide.image);
    this.slidesLoaded++;
  }

  public async preload(): Promise<void> {
    while (this.slides.length > this.slidesLoaded) {
      const slide = this.slides[this.slidesLoaded];
      this.load(slide);
    }
  }

  private async sync(): Promise<void> {
    const conn = new XMLHttpRequest();
    const payload = JSON.stringify({ index: this.index });
    conn.open('POST', window.location.href);
    conn.setRequestHeader('Content-Type', 'application/json');
    conn.send(payload);
  }

  public back(): void {
    this.index--;
    this.populate();
  } 

  public next(): void {
    this.index++;
    this.populate();
    if (this.index > this.highest) {
      this.sync();
    }
  }
}