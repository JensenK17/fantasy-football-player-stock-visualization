/**
 * API service for communicating with backend
 * Base URL: http://localhost:5000/api (dev)
 */

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';

export interface Player {
  player_id: string;
  name: string;
  position: string;
  team?: string;
}

export interface WeeklyStat {
  week: number;
  actual: number;
  projected: number;
  diff: number;
}

export interface PlayerStats {
  player_id: string;
  name: string;
  position: string;
  team: string;
  weekly_stats: WeeklyStat[];
  season_average: number;
}

export interface MarketStatus {
  current_week: number;
  is_market_open: boolean;
  locked_players: string[];
  time_until_close?: string;
}

/**
 * Get current NFL week number
 */
export async function getCurrentWeek(): Promise<number> {
  const response = await fetch(`${API_BASE_URL}/current-week`);
  const data = await response.json();
  return data.week;
}

/**
 * Get all available players
 * @param filters Optional filters (position, team, etc.)
 */
export async function getPlayers(filters?: any): Promise<Player[]> {
  const queryParams = filters ? `?${new URLSearchParams(filters)}` : '';
  const response = await fetch(`${API_BASE_URL}/players${queryParams}`);
  const data = await response.json();
  return data.players;
}

/**
 * Get a player's stats and projections
 * @param playerId Player ID
 */
export async function getPlayerStats(playerId: string): Promise<PlayerStats> {
  const response = await fetch(`${API_BASE_URL}/players/${playerId}/stats`);
  const data = await response.json();
  return data;
}

/**
 * Get current market status
 */
export async function getMarketStatus(): Promise<MarketStatus> {
  const response = await fetch(`${API_BASE_URL}/market-status`);
  const data = await response.json();
  return data;
}

/**
 * Get projections for a specific week
 * @param week Week number
 */
export async function getProjections(week: number): Promise<any> {
  const response = await fetch(`${API_BASE_URL}/week-projections/${week}`);
  const data = await response.json();
  return data;
}

