import React from 'react'
const PIXI = require('pixi.js')

class Game extends React.Component {
  constructor(props) {
    super(props);
    this.game = React.createRef()
    this.pixi_cnt = null
    this.app = new PIXI.Application({ backgroundColor: 0xaaaaaa });
    this.scale = 2
  }
  updatePixiCnt = (element) => {
    // the element is the DOM object that we will use as container to add pixi stage(canvas)
    this.pixi_cnt = element;
    //now we are adding the application to the DOM element which we got from the Ref.
    if(this.pixi_cnt && this.pixi_cnt.children.length<=0) {
      this.pixi_cnt.appendChild(this.app.view);
    }

    this.init()
  }
  background = (bgSize, inputSprite, type, forceSize) => {
    let sprite = inputSprite;
    let bgContainer = new PIXI.Container();
    let mask = new PIXI.Graphics().beginFill(0x8bc5ff).drawRect(0,0, bgSize.x, bgSize.y).endFill();
    bgContainer.mask = mask;
    bgContainer.addChild(mask);
    bgContainer.addChild(sprite);

    function resize() {
      let sp = {x:sprite.width,y:sprite.height};
      if(forceSize) sp = forceSize;
      let winratio = bgSize.x/bgSize.y;
      let spratio = sp.x/sp.y;
      let scale = 1;
      let pos = new PIXI.Point(0,0);
      if(type == 'cover' ? (winratio > spratio) : (winratio < spratio)) {
        //photo is wider than background
        scale = bgSize.x/sp.x;
        pos.y = -((sp.y*scale)-bgSize.y)/2
      } else {
        //photo is taller than background
        scale = bgSize.y/sp.y;
        pos.x = -((sp.x*scale)-bgSize.x)/2
      }

      sprite.scale = new PIXI.Point(scale,scale);
      sprite.position = pos;
    }

    resize();

    return {
      container: bgContainer,
      doResize: resize
    }
  }
  loadBackground = () => {
    let container = new PIXI.Container()
    let sprite = new PIXI.Sprite.from(this.app.loader.resources['world'].url)
    let slide = this.background({x:this.app.view.width, y:this.app.view.height}, sprite,'cover');
    container.addChild(slide.container);
    this.app.stage.addChild(container)
  }
  loadBackground2 = () => {
    this.world = new PIXI.Sprite.from(this.app.loader.resources['world'].url)
    this.world.width *= this.scale
    this.world.height *= this.scale
    this.app.stage.addChild(this.world)
  }
  doneLoading = e => {
    this.loadBackground2()
    this.createPlayerSheet()
    this.createPlayer()

    let dir = {
      up: false,
      down: false,
      left: false,
      right: false
    }

    document.onkeydown = function(evt) {
      switch(evt.key) {
        case 'w': dir.up = true
          break
        case 's': dir.down = true
          break
        case 'd': dir.right = true
          break
        case 'a': dir.left = true
          break
        default:
          break
      }
    }
    document.onkeyup = function(evt) {
      switch(evt.key) {
        case 'w': dir.up = false
          break
        case 's': dir.down = false
          break
        case 'd': dir.right = false
          break
        case 'a': dir.left = false
          break
        default:
          break
      }
    }
    window.player = this.player
    let speed = 2.5 * this.scale
    this.app.ticker.add((delta) => {
      if(dir.down) {
        if(!this.player.playing) {
          this.player.textures = this.playerSheet.walkDown;
          this.player.play()
        }

        this.world.y -= speed
      }
      if(dir.up) {
        if(!this.player.playing) {
          this.player.textures = this.playerSheet.walkUp;
          this.player.play()
        }
        this.world.y += speed
      }
      if(dir.right) {
        if(!this.player.playing) {
          this.player.textures = this.playerSheet.walkRight;
          this.player.play()
        }
        this.world.x -= speed
      }
      if(dir.left) {
        if(!this.player.playing) {
          this.player.textures = this.playerSheet.walkLeft;
          this.player.play()
        }
        this.world.x += speed
      }
    })
  }
  createPlayer = () => {
    this.player = new PIXI.AnimatedSprite(this.playerSheet.standDown)
    this.player.anchor.set(0.5)
    this.player.animationSpeed = .5
    this.player.loop = false
    this.player.x = this.app.view.height/2
    this.player.y = this.app.view.width/2
    this.app.stage.addChild(this.player)
    let scale = 0.6
    this.player.width *= scale * this.scale
    this.player.height *= scale * this.scale
    this.player.play()
  }
  createPlayerSheet = () => {
    let sheet = new PIXI.BaseTexture.from(this.app.loader.resources['agent'].url)
    let w = 30
    let h = 52
    let fr = 9
    this.playerSheet = {}
    function getChar(x,y) {
      return new PIXI.Rectangle(x*w, y*h, w, h)
    }
    this.playerSheet['standDown'] = [
      new PIXI.Texture(sheet,getChar(0,2))
    ]
    this.playerSheet['standUp'] = [
      new PIXI.Texture(sheet, getChar(0,0))
    ]
    this.playerSheet['standRight'] = [
      new PIXI.Texture(sheet, getChar(0,3))
    ]
    this.playerSheet['standLeft'] = [
      new PIXI.Texture(sheet, getChar(0,1))
    ]

    let names = ['walkUp', 'walkLeft', 'walkDown', 'walkRight']
    for(let n = 0; n < names.length; n++) {
      this.playerSheet[names[n]] = []
      for(let i = 0; i < fr; i++) {
        this.playerSheet[names[n]].push(new PIXI.Texture(sheet, getChar(i,n)))
      }
    }





  }
  init = () => {
    const app = this.app



    app.loader.add('agent','assets/agent.png')
    app.loader.add('world', 'assets/world.png')

    app.loader.load(this.doneLoading)

    const player = PIXI.Sprite.from(PIXI.Texture.WHITE);
    player.width = 200;
    player.height = 200;
    player.tint = 0xFF0000;
    player.position.x = 50
    player.position.y = 50
    //app.stage.addChild(player);


  }
  render() {
    return (<div ref={this.updatePixiCnt}></div>)
  }
}

export default Game
