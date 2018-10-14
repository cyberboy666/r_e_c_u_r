// Tenjix

#ifdef GL_ES
precision mediump float;
#endif

#define PI 3.1415926535897932384626433832795

uniform float u_time;
uniform vec2 u_resolution;

const float position = 0.0;
const float scale = 8.0;
const float intensity = 1.0;

float band(vec2 pos, float amplitude, float frequency) {
	float wave = scale * amplitude * sin(2.0 * PI * frequency * pos.x + u_time) / 6.05;
	float light = clamp(amplitude * frequency * 0.002, 0.001 + 0.001 / scale, 5.0) * scale / abs(wave - pos.y);
	return light;
}

void main( void ) {

	vec3 color = vec3(0., 0.5, 1.0);
	color = color == vec3(0.0)? vec3(0.10, 0.5, 10.0) : color;
	vec2 pos = (gl_FragCoord.xy / u_resolution.xy);
	pos.y += - 0.5 - position;
	
	float spectrum = 0.0;

	spectrum += band(pos, 0.1, 10.0);
	spectrum += band(pos, 0.2, 8.0);
	spectrum += band(pos, 0.10, 5.0);
	spectrum += band(pos, 0.09, 3.0);
	spectrum += band(pos, 0.8, 2.0);
	spectrum += band(pos, 1.0, 1.0);
	
	gl_FragColor = vec4(color * spectrum, spectrum);
	
}
