const URL = process.env.NODE_ENV === 'production' ? undefined : 'http://housemusic.local:5001';
export const socket = io(URL);