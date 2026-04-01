/**
 * @vitest-environment jsdom
 */
import { describe, it, expect } from 'vitest';
import { render, screen, fireEvent } from '@testing-library/react';
import '@testing-library/jest-dom';
import App from './App';

describe('SoFake Frontend Unit Tests', () => {
  
  // 测试点 1：字数统计逻辑
  it('should calculate remaining characters correctly', () => {
    render(<App />);
    const textarea = screen.getByPlaceholderText(/Paste the ground truth here/i);
    
    // 输入一段文本
    fireEvent.change(textarea, { target: { value: 'Hello SoFake' } });
    
    // 验证显示是否为 "12 / 6,000 chars"
    expect(screen.getByText(/12 \/ 6,000 chars/i)).toBeDefined();
  });

  // 测试点 2：角色比例总和验证
  it('should show warning when role mix does not sum to 100%', () => {
    render(<App />);
    
    expect(screen.queryByText(/Role mix should sum to 100%/i)).toBeNull();

    // 重点：改用这种方式寻找。因为 Devin 没有给输入框绑定 Label，
    // 我们直接通过它的初始显示值（35）来找到第一个匹配的输入框。
    const allNumberInputs = screen.getAllByRole('spinbutton');
    // 根据页面结构，前三个是 AgentCount, Seed, Steps，第四个是 Spreaders
    const spreaderInput = allNumberInputs[3]; 

    fireEvent.change(spreaderInput, { target: { value: '50' } });

    expect(screen.getByText(/Role mix should sum to 100%/i)).toBeDefined();
  });

  // 测试点 3：Start Simulation 按钮状态
  it('should disable Start Simulation button if ground truth is empty', () => {
    render(<App />);
    const runButton = screen.getByText(/Start Simulation/i);
    
    // 初始状态为空，按钮应被禁用
    expect(runButton.closest('button')).toBeDisabled();

    // 输入内容后按钮应启用
    const textarea = screen.getByPlaceholderText(/Paste the ground truth here/i);
    fireEvent.change(textarea, { target: { value: 'Valid Ground Truth' } });
    expect(runButton.closest('button')).not.toBeDisabled();
  });

  // 测试点 4：页面导航
  it('should navigate to Graph View when sidebar item is clicked', () => {
    render(<App />);
    
    const graphLink = screen.getByText(/Graph View/i);
    fireEvent.click(graphLink);

    // 验证是否显示了 Graph View 的占位内容
    expect(screen.getByText(/Hook this to your run results/i)).toBeDefined();
  });
});