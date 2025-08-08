import React, { useState, useEffect } from 'react';
import { render, Box, Text, useApp } from 'ink';
import TextInput from 'ink-text-input';
import axios from 'axios';
import WebSocket from 'ws';

const BACKEND_URL = 'http://localhost:8000';

// --- Components ---
const OutputPanel = ({ history }) => (
    <Box borderStyle="round" padding={1} flexDirection="column" flexGrow={1}>
        {history.map((item, index) => {
            let color = 'white';
            if (item.type === 'error') color = 'red';
            if (item.type === 'system') color = 'blue';
            if (item.type === 'user') color = 'green';

            return (
                <Box key={index}>
                    <Text color={color}>{item.data}</Text>
                </Box>
            );
        })}
    </Box>
);

const NotificationPanel = ({ notification }) => {
    if (!notification) return null;
    return (
        <Box borderStyle="round" paddingX={1} borderColor="yellow">
            <Text color="yellow">{notification.title}: </Text>
            <Text>{notification.message}</Text>
        </Box>
    );
};

// --- Main App ---
const App = () => {
    const { exit } = useApp();
    const [history, setHistory] = useState([{ type: 'system', data: 'Initializing and connecting to backend...' }]);
    const [connectionId, setConnectionId] = useState(null);
    const [inputValue, setInputValue] = useState('');
    const [notification, setNotification] = useState(null);

    const addHistory = (type, data) => {
        setHistory(prev => [...prev, { type, data }]);
    };

    useEffect(() => {
        const connect = async () => {
            try {
                addHistory('system', 'Requesting connection ID...');
                const response = await axios.post(`${BACKEND_URL}/api/v1/connect`);
                const { connection_id } = response.data;
                setConnectionId(connection_id);
                addHistory('system', `Connection ID received. Establishing WebSocket connection...`);

                const socket = new WebSocket(`ws://localhost:8000/ws/${connection_id}`);

                socket.on('open', () => addHistory('system', 'Connection established. Ready for input.'));

                socket.on('message', (data) => {
                    const message = JSON.parse(data.toString());
                    if (message.type === 'diff') {
                        addHistory('system', `--- PROPOSED CHANGE for ${message.file_path} ---`);
                        addHistory('diff', message.data);
                        setNotification({ title: 'Confirm', message: 'Apply this diff? (yes/no)' });
                    } else {
                        addHistory(message.type, message.data);
                    }
                });

                socket.on('close', () => addHistory('error', 'Connection to server lost. Please restart.'));
                socket.on('error', (error) => addHistory('error', `Connection error: ${error.message}. Please restart.`));

            } catch (error) {
                addHistory('error', `Failed to connect to backend: ${error.message}`);
            }
        };
        connect();
    }, []);

    const handleSubmit = async () => {
        if (!connectionId || !inputValue) return;
        
        addHistory('user', `> ${inputValue}`);
        const url = `${BACKEND_URL}/api/v1/input/${connectionId}`;
        try {
            await axios.post(url, { text: inputValue });
            setInputValue('');
        } catch (error) {
            addHistory('error', `Error sending command: ${error.message}`);
        }
    };

    return (
        <Box flexDirection="column" padding={1} height="100%">
            <OutputPanel history={history} />
            <NotificationPanel notification={notification} />
            <Box>
                <Text color="green">? </Text>
                <TextInput 
                    value={inputValue} 
                    onChange={setInputValue} 
                    onSubmit={handleSubmit}
                    placeholder="Type your command or prompt..."
                />
            </Box>
        </Box>
    );
};

render(React.createElement(App));
