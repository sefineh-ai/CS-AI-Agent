import axios from "axios";

export const fetchChatResponse = async (query: string) => {
    const response = await axios.get(`http://localhost:8000/chat/`, { params: { query } });
    return response.data.response;
};

export default fetchChatResponse