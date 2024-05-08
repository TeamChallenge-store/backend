import { FC } from 'react';

type TEmpty = {
  title: string;
};
const Empty: FC<TEmpty> = props => {
  return (
    <div
      style={{
        textAlign: 'center',
        height: '100%',
        display: 'flex',
        alignItems: 'center',
        backgroundColor: 'grey',
        justifyContent: 'center',
        borderRadius: '10px',
      }}
    >
      <h1>{props.title}</h1>
    </div>
  );
};

export { Empty };
