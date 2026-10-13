import axios,{type AxiosInstance,type AxiosError,type InternalAxiosRequestConfig,type AxiosResponse} from 'axios';
import { ElMessage } from 'element-plus';

const service:AxiosInstance=axios.create({
    baseURL:'/api',
    timeout:3000,
    headers:{
        "Content-Type":"application/json"
    }
})

service.interceptors.request.use(
    (config:InternalAxiosRequestConfig)=>{
        const token = localStorage.getItem('token');
        if(token&&config.headers){
            config.headers.Authorization=`Bearer ${token}`
        }
        return config;
    },
    (error:AxiosError)=>{
        ElMessage.error(error.message);
        return Promise.reject(error);
    }
)

service.interceptors.response.use(
    (response:AxiosResponse)=>{
        // 成功直接返回data，不用每次都重新取
        return response.data;
    },
    (error:AxiosError<any>)=>{
       const status = error.response?.status
       const detail = error.response?.data?.detail || "请求失败"

       if(status===401){
        localStorage.removeItem('token')
        ElMessage.error('登录过期，请重新登录')
        if(window.location.pathname!=='/login'){
            window.location.href='/login'
        }
       } else if(status===403){
        ElMessage.error('没有权限访问')
       } else if(status===404){
        ElMessage.error('请求资源不存在')
       }else if(status===422){
        const errors = error.response?.data?.detail
        if(Array.isArray(errors)){
            ElMessage.error(errors[0]?.msg || '请求参数错误')
        }else{
            ElMessage.error('请求参数错误')
        }
       }else if(status===500){
        ElMessage.error('服务器内部错误')
       }else{
        ElMessage.error(typeof detail === 'string' ? detail:'请求失败')
       }
       return Promise.reject(error);
    }
)

const request = service as unknown as {
    get<T = any>(url: string, config?: any): Promise<T>
    post<T = any>(url: string, data?: any, config?: any): Promise<T>
    put<T = any>(url: string, data?: any, config?: any): Promise<T>
    patch<T = any>(url: string, data?: any, config?: any): Promise<T>
    delete<T = any>(url: string, config?: any): Promise<T>
}

export default request