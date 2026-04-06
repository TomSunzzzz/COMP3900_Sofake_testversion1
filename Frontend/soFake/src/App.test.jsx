/**
 * @vitest-environment jsdom
 */
//import { describe, it, expect } from 'vitest';
import { render, screen, fireEvent } from '@testing-library/react';
import '@testing-library/jest-dom';
import App from './App';

describe('SoFake Frontend Unit Tests', () => {
  
  // Test Case 1: Character count logic
  it('should calculate remaining characters correctly', () => {
    render(<App />);
    const textarea = screen.getByPlaceholderText(/Paste the ground truth here/i);
    
    // Input a string of text
    fireEvent.change(textarea, { target: { value: 'Hello SoFake' } });
    
    // Verify if the display shows "12 / 6,000 chars"
    expect(screen.getByText(/12 \/ 6,000 chars/i)).toBeDefined();
  });

  // Test Case 2: Role ratio sum validation
  it('should show warning when role mix does not sum to 100%', () => {
    render(<App />);
    
    expect(screen.queryByText(/Role mix should sum to 100%/i)).toBeNull();

    // Note: Since inputs aren't explicitly bound to labels, 
    // we retrieve all spinbuttons and select by index.
    const allNumberInputs = screen.getAllByRole('spinbutton');
    
    // Based on the layout: the first three are AgentCount, Seed, and Steps; 
    // the fourth (index 3) is Spreaders.
    const spreaderInput = allNumberInputs[3]; 

    fireEvent.change(spreaderInput, { target: { value: '50' } });

    expect(screen.getByText(/Role mix should sum to 100%/i)).toBeDefined();
  });

  // Test Case 3: Start Simulation button state
  it('should disable Start Simulation button if ground truth is empty', () => {
    render(<App />);
    const runButton = screen.getByText(/Start Simulation/i);
    
    // Initial state is empty; button should be disabled
    expect(runButton.closest('button')).toBeDisabled();

    // Button should be enabled after entering valid content
    const textarea = screen.getByPlaceholderText(/Paste the ground truth here/i);
    fireEvent.change(textarea, { target: { value: 'Valid Ground Truth' } });
    expect(runButton.closest('button')).not.toBeDisabled();
  });

  // Test Case 4: Page navigation
  it('should navigate to Graph View when sidebar item is clicked', () => {
    render(<App />);
    
    const graphLink = screen.getByText(/Graph View/i);
    fireEvent.click(graphLink);

    // Verify if the placeholder content for Graph View is displayed
    expect(screen.getByText(/Hook this to your run results/i)).toBeDefined();
  });
});