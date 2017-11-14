//From: https://solutiondesign.com/blog/-/blogs/webgl-and-three-js-texture-mappi-1/

var camera;
var scene;
var renderer;
var cube;


function init() {

    scene = new THREE.Scene();
		scene.background = new THREE.Color( 0xf0f0f0 );

    camera = new THREE.PerspectiveCamera( 20, window.innerWidth / window.innerHeight, 10, 1000);
    // camera = new THREE.OrthographicCamera(-50,50,50,-50, 1, 200);

    var light = new THREE.DirectionalLight( 0xffffff );
    light.position.set( 0, 50, 300).normalize();
    scene.add(light);

		var geometry = new THREE.BoxGeometry( 50, 2, 40);
		var material1 = new THREE.MeshPhongMaterial( {
			color: 0x000000,
			shininess: 3
		} );
		var material_display = new THREE.MeshPhongMaterial( {
			map: new THREE.TextureLoader().load('img/display-side.png'),
			shininess: 20
		} );
		var material_sensors = new THREE.MeshPhongMaterial( {
			map: new THREE.TextureLoader().load('img/sensors-side.png'),
			shininess: 20
		} );
		cube = new THREE.Mesh( geometry,
			[material1,material1,material_display,material_sensors,material1,material1,]
		);
    cube.position.z = -250;
		scene.add( cube );

    renderer = new THREE.WebGLRenderer();
    renderer.setSize( window.innerWidth, window.innerHeight );
    document.body.appendChild( renderer.domElement );

    window.addEventListener( 'resize', onWindowResize, false );

    render();
}

function animate() {
    cube.rotation.x += 0.01;
    // cube.rotation.y += .02;

    render();
    requestAnimationFrame( animate );
}

function render() {
    renderer.render( scene, camera );
}

function onWindowResize() {
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize( window.innerWidth, window.innerHeight );
    render();
}


init();

var ws = new WebSocket("ws://127.0.0.1:5678/");

ws.onmessage = function (event) {
	orientation = JSON.parse(event.data);
	// console.log(orientation);
	cube.rotation.z = orientation[0]/180*3.141592;  // Roll
	cube.rotation.x = orientation[1]/180*3.141592;  // Pitch
	cube.rotation.y = -orientation[2]/180*3.141592;  // Yaw
  render();
};
