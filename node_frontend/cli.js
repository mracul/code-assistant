import React from 'react';
import { render, Box, Text } from 'ink';
import TextInput from 'ink-text-input';
import axios from 'axios';

const BACKEND_URL = 'http://localhost:8000';

const App = () => {
    const [query, setQuery] = React.useState('');
    const [logs, setLogs] = React.useState([]);

    const handleSubmit = async (value) => {
        const newLogs = [...logs, `> ${value}`];
        setLogs(newLogs);
        setQuery('');

        if (value.toLowerCase() === 'ping') {
            try {
                const response = await axios.get(`${BACKEND_URL}/api/v1/ping`);
                const status = response.data.status;
                setLogs(prevLogs => [...prevLogs, `Backend status: ${status}`]);
            } catch (error) {
                setLogs(prevLogs => [...prevLogs, `Error connecting to backend: ${error.message}`]);
            }
        }
    };

    return (
        <Box flexDirection="column" padding={1} width="100%">
            <Box borderStyle="round" paddingX={2}>
                <Text bold color="blue">Agentic Code Assistant</Text>
            </Box>
            <Box flexGrow={1} marginTop={1} flexDirection="column">
                {logs.map((log, i) => (
                    <Text key={i}>{log}</Text>
                ))}
            </Box>
            <Box>
                <Text>&gt; </Text>
                <TextInput
                    value={query}
                    onChange={setQuery}
                    onSubmit={handleSubmit}
                />
            </Box>
        </Box>
    );
};

render(React.createElement(App));

export default App;
