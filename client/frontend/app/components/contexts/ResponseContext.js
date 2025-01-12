import { createContext, useState, useContext } from 'react';

export const ResponseContext = createContext();

export const useResponse = () => {
    return useContext(ResponseContext);
};

export const ResponseProvider = ({ children }) => {
    const [responseData, setResponseData] = useState([]);

    return (
        <ResponseContext.Provider value={{ responseData, setResponseData }}>
            {children}
        </ResponseContext.Provider>
    );
};
