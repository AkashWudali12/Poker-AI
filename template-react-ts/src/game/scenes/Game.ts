import { EventBus } from '../EventBus';
import { Scene } from 'phaser';

export class Game extends Scene
{
    camera: Phaser.Cameras.Scene2D.Camera;
    background: Phaser.GameObjects.Image;
    gameText: Phaser.GameObjects.Text;

    constructor ()
    {
        super('Game');
    }

    create() {
        this.camera = this.cameras.main;
    
        // Add background image and set it to cover the entire game area
        this.background = this.add.image(512, 384, 'background');

        this.background.setScale(Math.max(
            this.cameras.main.width / this.background.width,
            this.cameras.main.height / this.background.height
        ));

        const two_of_clubs = this.add.image(512, 384, '2_of_clubs')
        two_of_clubs.setScale(0.25)

        this.background = two_of_clubs
    
        EventBus.emit('current-scene-ready', this);
    }

    changeScene ()
    {
        this.scene.start('GameOver');
    }
}
