// this is the default vert file used by glslVeiwer
#ifdef GL_ES
precision mediump float;
#endif
uniform mat4 u_modelViewProjectionMatrix;

attribute vec4  a_position;
attribute vec4  a_color;
attribute vec3  a_normal;
attribute vec2  a_texcoord;

varying vec4    v_position;
varying vec4    v_color;
varying vec3    v_normal;
varying vec2    v_texcoord;


#ifdef SHADOW_MAP
uniform mat4    u_lightMatrix;
varying vec4    v_lightcoord;
#endif

#ifdef MODEL_HAS_TANGENTS
varying mat3    v_tangentToWorld;
#endif

void main(void) {

    v_position = a_position;
    v_color = a_color;
    v_normal = a_normal;
    v_texcoord = a_texcoord;

#ifdef MODEL_HAS_TANGENTS
    vec3 worldTangent = a_tangent.xyz;
    vec3 worldBiTangent = cross(v_normal, worldTangent) * sign(a_tangent.w);
    v_tangentToWorld = mat3(normalize(worldTangent), normalize(worldBiTangent), normalize(v_normal));
#endif
    
#ifdef SHADOW_MAP
    v_lightcoord = u_lightMatrix * v_position;
#endif
    
    gl_Position = u_modelViewProjectionMatrix * v_position;
}

