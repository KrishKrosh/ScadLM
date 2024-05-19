import axios from "axios";
import { downloadAxiosResponse } from "../utils";

const BASE_URL = "http://127.0.0.1:5001";

export function getCadShapes(query: string, uuid: string | null = null) {
  let config = {
    method: 'get',
    maxBodyLength: Infinity,
    headers: { "Content-Type": "application/json" },
    url: `${BASE_URL}/cad`,
    params: { query, uuid },
  };

  return axios.request(config)
    .then(response => response.data)
    .catch(error => console.error(error));
}

export function getCadDownload(generation_id: string, iteration: string, file_type: "stl" | "step") {
  let config = {
    method: 'get',
    maxBodyLength: Infinity,
    responseType: 'arraybuffer',
    headers: { "Content-Type": "application/json" },
    url: `${BASE_URL}/models/generated/${generation_id}/${iteration}/output.${file_type}`,
  };

  return axios.request(config)
    .then(response => downloadAxiosResponse(`${generation_id}_${iteration}.${file_type}`, response))
    .catch(error => console.error(error));
}

export function getGeneratedFiles(generation_id: string, iteration: string) {
  let config = {
    method: 'get',
    headers: { "Content-Type": "application/json" },
    url: `${BASE_URL}/files/${generation_id}/${iteration}`,
  };

  return axios.request(config)
    .then(response => response.data)
    .catch(error => console.error(error));
}
