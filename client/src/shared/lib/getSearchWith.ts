type TParam = string | number;

type TParams = {
  [key: string]: TParam[] | TParam | null;
};

const getSearchWith = (params: TParams, search?: string | URLSearchParams) => {
  const newParams = new URLSearchParams(search);

  Object.entries(params).forEach(([key, value]) => {
    if (value === null) {
      newParams.delete(key);
    } else if (Array.isArray(value)) {
      newParams.delete(key);
      value.forEach(item => newParams.append(key, item.toString()));
    } else {
      newParams.set(key, value.toString());
    }
  });

  return newParams;
};

export { getSearchWith };
