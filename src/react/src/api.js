// Thin wrapper around fetch. In development the Vite proxy sends /api to FastAPI.
// In production set VITE_API_BASE to the API origin, for example https://api.example.com.
const BASE = import.meta.env.VITE_API_BASE ?? "";

export async function getJson(path) {
  const response = await fetch(`${BASE}${path}`, {
    headers: { Accept: "application/json" },
  });
  if (!response.ok) {
    throw new Error(`Request failed: ${response.status}`);
  }
  return response.json();
}

export function listItems(limit = 12) {
  return getJson(`/api/v1/content/items?limit=${limit}`);
}
