export interface QueryRequest {
    query: string;
    filter?: string | string[];
    offset?: number;
    limit?: number;
    fields?: string[];
    sort?: string | string[];
    facet?: Record<string, unknown>;
    queries?: unknown;
}

export interface QueryResponse<Document> {
    responseHeader: {
        status: number;
        QTime: number;
        params: Record<string, string | number>;
    };
    response: {
        numFound: number;
        start: number;
        numFoundExact: boolean;
        docs: Document[];
    };
}

export interface GetResponse<Document> {
    doc: Document;
}
