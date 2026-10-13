import { defineStore } from "pinia";
import { ref, computed } from "vue";
import {
    login,
    getMe,
    type LoginRequest,
    type UserInfoResponse,
} from "@/api/auth";

export const useUserStore = defineStore("user", () => {
    const token = ref<string>(localStorage.getItem("token") || "");
    const userInfo = ref<UserInfoResponse | null>(null);

    const isLoggedIn = computed(() => !!token.value);
    const role = computed(() => userInfo.value?.role || null);

    const loginAction = async (data: LoginRequest) => {
        const res = await login(data);
        token.value = res.access_token;
        localStorage.setItem("token", res.access_token);

        await fetchUserInfo();
    };

    const fetchUserInfo = async () => {
        if (!token.value) return;
        try {
            userInfo.value = await getMe();
        } catch (e) {
            // token 失效，清掉
            logout();
        }
    };

    const logout = () => {
        token.value = "";
        localStorage.removeItem("token");
        userInfo.value = null;
    };

    return {
        token,
        userInfo,
        isLoggedIn,
        role,
        loginAction,
        fetchUserInfo,
        logout,
    };
});
