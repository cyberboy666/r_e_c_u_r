#ifdef GL_ES
precision mediump float;
#endif

uniform float u_time;
uniform float u_x0;

void main() {
	gl_FragColor = vec4(sin(1000.0*u_x0*u_time),0.0,0.0,1.0);
}
