export interface QueryRequest {
    query: string;
    filter?: string | string[];
    offset?: number;
    limit?: number;
    fields?: string[];
    sort?: string | string[];
    facet?: Record<string, unknown>;
    queries?: unknown;
    params?: Record<string, string | number>;
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
    spellcheck?: {
        suggestions: (
            | string
            | {
                  numFound: number;
                  startOffset: number;
                  endOffset: number;
                  suggestion: string[];
              }
        )[];
        collations: string[];
    };
    highlighting?: Record<string, Record<string, string[]>>;
}

export interface GetResponse<Document> {
    doc: Document;
}

export interface MLTResponse<Document> {
    match: {
        numFound: number;
        start: number;
        numFoundExact: boolean;
        docs: Document[];
    };
    response: {
        numFound: number;
        start: number;
        numFoundExact: boolean;
        docs: Document[];
    };
}
