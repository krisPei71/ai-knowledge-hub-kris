import request from "./request";

export interface LoginRequest {
    username:string;
    password:string
}

export interface TokenResponse{
    access_token:string;
    token_type:string;
}

export interface UserInfoResponse{
    id:number;
    username:string
    password:string;
    role:'admin' | 'handler' | 'reporter';
    created_at:string;
}

export function login(data:LoginRequest){
    return request.post<TokenResponse>('/auth/login',data)
}

export function getMe(){
    return request.get<UserInfoResponse>('/auth/me')
}