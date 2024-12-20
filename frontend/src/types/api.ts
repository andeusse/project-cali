export type resp<T> = {
  model: T;
};

export type errorResp = {
  message: string;
};

export type loginOutput = {
  password: string;
};

export type loginInput = {
  succeed: boolean;
};
