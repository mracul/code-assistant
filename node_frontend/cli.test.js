import React from 'react';
import {render} from 'ink-testing-library';
import App from './cli.js';

// Mock axios to prevent actual network requests
jest.mock('axios');

describe('Agentic Code Assistant TUI', () => {
    // This is a workaround for a known issue with Jest and Ink
    beforeAll(() => {
        process.stdout.columns = 80;
        process.stdout.rows = 24;
    });

    it('should render the header', () => {
        const {lastFrame} = render(React.createElement(App));
        expect(lastFrame()).toContain('Agentic Code Assistant');
    });

    it('should echo user input to the log', () => {
        const {stdin, lastFrame} = render(React.createElement(App));

        stdin.write('test command\r');

        expect(lastFrame()).toContain('> test command');
    });
});
