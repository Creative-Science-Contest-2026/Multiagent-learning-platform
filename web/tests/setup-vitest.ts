import "@testing-library/jest-dom/vitest";

if (!process.env.NEXT_PUBLIC_API_BASE && !process.env.NEXT_PUBLIC_API_BASE_EXTERNAL) {
  process.env.NEXT_PUBLIC_API_BASE = "http://localhost:8001";
}
