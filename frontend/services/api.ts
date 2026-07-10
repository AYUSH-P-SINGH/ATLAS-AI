const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

interface RequestOptions extends RequestInit {
  params?: Record<string, string>;
}

export class APIError extends Error {
  status: number;
  data: any;

  constructor(message: string, status: number, data?: any) {
    super(message);
    this.name = "APIError";
    this.status = status;
    this.data = data;
  }
}

export async function apiClient<T>(path: string, options: RequestOptions = {}): Promise<T> {
  const { params, headers, ...rest } = options;

  // Construct URL with query parameters if present
  let url = `${API_BASE_URL}${path.startsWith("/") ? path : `/${path}`}`;
  if (params) {
    const searchParams = new URLSearchParams();
    Object.entries(params).forEach(([key, val]) => {
      if (val !== undefined && val !== null) {
        searchParams.append(key, val);
      }
    });
    const queryString = searchParams.toString();
    if (queryString) {
      url += `?${queryString}`;
    }
  }

  // Set default headers
  const defaultHeaders: Record<string, string> = {};
  
  if (!(rest.body instanceof FormData)) {
    defaultHeaders["Content-Type"] = "application/json";
  }

  // Attach local client Bearer token if stored in localStorage
  if (typeof window !== "undefined") {
    const token = localStorage.getItem("token");
    if (token) {
      defaultHeaders["Authorization"] = `Bearer ${token}`;
    }
  }

  const mergedHeaders = {
    ...defaultHeaders,
    ...headers,
  };

  const fetchOptions: RequestInit = {
    ...rest,
    headers: mergedHeaders,
    credentials: "include", // Essential for HttpOnly cookie authentication
  };

  try {
    const response = await fetch(url, fetchOptions);

    if (response.status === 204) {
      return {} as T;
    }

    const contentType = response.headers.get("content-type");
    let responseData: any = null;
    
    if (contentType && contentType.includes("application/json")) {
      responseData = await response.json();
    } else {
      responseData = await response.text();
    }

    if (!response.ok) {
      const errorMsg =
        responseData?.detail || responseData?.message || `Request failed with status ${response.status}`;
      throw new APIError(errorMsg, response.status, responseData);
    }

    return responseData as T;
  } catch (error) {
    if (error instanceof APIError) {
      throw error;
    }
    // Handle network or parsing errors
    logger_error(error);
    throw new APIError("Network connectivity issue. Please try again.", 0);
  }
}

function logger_error(error: any) {
  console.error("API Client invocation failed:", error);
}
