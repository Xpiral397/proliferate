import axiosClient from "../axios";
import {getUserToken} from "./getUserToken";


export async function getProfile(id) {
    try {
        const response=await axiosClient().get(`user/profile/${id}`,
            {
                headers: {
                    Authorization: `Bearer ${getUserToken()}`
                }
            });
        if(response.statusCode===401) {
            return {status: 401, message: response.detail}
        }
        return {data: response.data, status: 200};
    } catch(errr) {
        return {
            status: 500,
            message: errr?.response?.data?.error||errr?.response?.data?.message||errr?.response?.data?.detail||'Unable To Process Your Request'
        }
    }
}