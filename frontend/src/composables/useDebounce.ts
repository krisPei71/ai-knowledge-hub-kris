import {ref,watch,type Ref} from 'vue'

export function useDebounce<T>(
    source:Ref<T>,
    callback:(value:T)=>void,
    delay:number=800
){
    const timer = ref<number|null>(null)

    watch(
        source,
        (newVal)=>{
            if(timer.value!=null){
                clearTimeout(timer.value)
            }
            timer.value=window.setTimeout(()=>{
                callback(newVal)
            },delay)
        }
    )
}