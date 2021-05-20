#version 120

vec4 _l_position1;
vec3 _l_interpolate1;
vec4 _l_texcoord11;
vec3 _l_surface_pos1;
vec2 _l_texcoord01;
vec2 _l_alpha_uv1;
vec3 _l_normal1;
uniform vec4 fogexpdensity;
uniform vec4 map;
uniform vec4 alphamap;
uniform vec4 trans_view_to_world[4];
uniform vec4 trans_model_to_view[4];
uniform vec4 trans_model_to_apiclip[4];
vec4 _r0010;
vec4 _r0020;
vec4 _r0030;
float _TMP39;
float _x0040;
vec4 _r0044;

 // main procedure, the original name was vshader
void main()
{

    vec4 _vertex;

    _vertex.xyz = gl_Vertex.xyz;
    _vertex.w = 1.00000000E+00;
    _r0010.x = dot(trans_model_to_apiclip[0], _vertex);
    _r0010.y = dot(trans_model_to_apiclip[1], _vertex);
    _r0010.z = dot(trans_model_to_apiclip[2], _vertex);
    _r0010.w = dot(trans_model_to_apiclip[3], _vertex);
    _l_normal1 = gl_Normal;
    _l_surface_pos1 = gl_Vertex.xyz;
    _l_texcoord01 = gl_MultiTexCoord0.xy;
    _r0020.x = dot(trans_model_to_view[0], _vertex);
    _r0020.y = dot(trans_model_to_view[1], _vertex);
    _r0020.z = dot(trans_model_to_view[2], _vertex);
    _r0020.w = dot(trans_model_to_view[3], _vertex);
    _r0030.x = dot(trans_view_to_world[0], _r0020);
    _r0030.y = dot(trans_view_to_world[1], _r0020);
    _l_interpolate1.xy = (_r0030.xy - map.xy)*map.zw;
    _l_alpha_uv1.xy = (_r0030.xy - alphamap.xy)*alphamap.zw;
    _x0040 = -(fogexpdensity.x*_r0020.y);
    _TMP39 = pow(2.71828198E+00, _x0040);
    _l_interpolate1.z = 1.00000000E+00 - _TMP39;
    _r0044.x = dot(vec4( 5.00000000E-01, 0.00000000E+00, 0.00000000E+00, 5.00000000E-01), _r0010);
    _r0044.y = dot(vec4( 0.00000000E+00, 5.00000000E-01, 0.00000000E+00, 5.00000000E-01), _r0010);
    _r0044.z = dot(vec4( 0.00000000E+00, 0.00000000E+00, 5.00000000E-01, 5.00000000E-01), _r0010);
    _r0044.w = dot(vec4( 0.00000000E+00, 0.00000000E+00, 0.00000000E+00, 1.00000000E+00), _r0010);
    _l_texcoord11 = _r0044;
    _l_position1 = _r0010;
    gl_TexCoord[2].xyz = gl_Normal;
    gl_TexCoord[5].xy = _l_alpha_uv1;
    gl_TexCoord[0].xy = gl_MultiTexCoord0.xy;
    gl_TexCoord[3].xyz = gl_Vertex.xyz;
    gl_TexCoord[1] = _r0044;
    gl_TexCoord[4].xyz = _l_interpolate1;
    gl_Position = _r0010;
} // main end
