// ------------------------------------------------------------
// Truncated Octahedron Voxel Demo (Three.js)
// Drop-in landing page visual
// ------------------------------------------------------------

import * as THREE from "three";
import { ConvexGeometry } from "three/examples/jsm/geometries/ConvexGeometry.js";

// ------------------------------------------------------------
// Scene setup
// ------------------------------------------------------------

const scene = new THREE.Scene();
scene.background = null;

const camera = new THREE.PerspectiveCamera(
  60,
  window.innerWidth / window.innerHeight,
  0.1,
  1000
);
camera.position.set(12, 12, 12);
camera.lookAt(0, 0, 0);

const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
renderer.setSize(window.innerWidth, window.innerHeight);
renderer.setPixelRatio(window.devicePixelRatio);
renderer.setClearColor(0x000000, 0);
renderer.domElement.className = "bg-canvas";
renderer.domElement.setAttribute("aria-hidden", "true");
document.body.appendChild(renderer.domElement);

// ------------------------------------------------------------
// Lighting
// ------------------------------------------------------------

scene.add(new THREE.AmbientLight(0xffffff, 0.4));

const dirLight = new THREE.DirectionalLight(0xffffff, 0.8);
dirLight.position.set(10, 20, 10);
scene.add(dirLight);

// ------------------------------------------------------------
// Truncated Octahedron Geometry (triangulated, engine-safe)
// ------------------------------------------------------------

const vertices = new Float32Array([
  2,0,1,   2,0,-1,  -2,0,1,  -2,0,-1,
  1,2,0,  -1,2,0,   1,-2,0, -1,-2,0,
  0,1,2,   0,-1,2,  0,1,-2, 0,-1,-2,
  1,0,2,  -1,0,2,   1,0,-2,-1,0,-2,
  0,2,1,   0,2,-1,  0,-2,1, 0,-2,-1,
  2,1,0,   2,-1,0, -2,1,0, -2,-1,0,
]);

const indices = [
  // Squares
  0,20,16,  0,16,12,
  1,21,17,  1,17,14,
  2,22,16,  2,16,13,
  3,23,17,  3,17,15,
  4,16,20,  4,20,5,
  6,21,17,  6,17,7,

  // Hexagons
  0,12,8,  0,8,16,  16,8,5,  5,8,4,
  2,13,9,  2,9,16,  16,9,4,  4,9,5,
  1,14,11, 1,11,17, 17,11,7, 7,11,6,
  3,15,10, 3,10,17, 17,10,6, 6,10,7,
  4,8,12,  4,12,20, 20,12,0, 0,12,4,
  5,8,12,  5,12,16, 16,12,0, 0,12,5,
];

// Geometry
const points = [];
for (let i = 0; i < vertices.length; i += 3) {
  points.push(new THREE.Vector3(
    vertices[i],
    vertices[i + 1],
    vertices[i + 2]
  ));
}

const geometry = new ConvexGeometry(points);
geometry.computeVertexNormals();

// ------------------------------------------------------------
// Material
// ------------------------------------------------------------

const material = new THREE.MeshStandardMaterial({
  color: 0x6fa8dc,
  flatShading: true,
  metalness: 0.1,
  roughness: 0.6,
});

// ------------------------------------------------------------
// Instanced voxel grid (BCC lattice)
// ------------------------------------------------------------

const GRID = 2;
const OFFSETS = [];

for (let x = -GRID; x <= GRID; x++) {
  for (let y = -GRID; y <= GRID; y++) {
    for (let z = -GRID; z <= GRID; z++) {
      OFFSETS.push(new THREE.Vector3(4*x, 4*y, 4*z));
      OFFSETS.push(new THREE.Vector3(4*x+2, 4*y+2, 4*z+2));
    }
  }
}

const mesh = new THREE.InstancedMesh(
  geometry,
  material,
  OFFSETS.length
);

const m = new THREE.Matrix4();
OFFSETS.forEach((p, i) => {
  m.makeTranslation(p.x, p.y, p.z);
  mesh.setMatrixAt(i, m);
});

scene.add(mesh);

// ------------------------------------------------------------
// Animation loop
// ------------------------------------------------------------

function animate() {
  requestAnimationFrame(animate);
  mesh.rotation.y += 0.002;
  mesh.rotation.x += 0.001;
  renderer.render(scene, camera);
}

animate();

// ------------------------------------------------------------
// Resize handling
// ------------------------------------------------------------

window.addEventListener("resize", () => {
  camera.aspect = window.innerWidth / window.innerHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(window.innerWidth, window.innerHeight);
});
