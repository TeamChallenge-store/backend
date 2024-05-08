import { FC } from 'react';
import cn from 'classnames';

import { THandleOption } from '../types/THandleOption';

import css from '../CustomSelect.module.scss';

type TOptionButtonProps = {
  options: [string, string];
  selectedOption: string;
  onClick: (args: THandleOption) => void;
};

const OptionButton: FC<TOptionButtonProps> = ({
  selectedOption,
  onClick,
  options,
}) => {
  const [value, option] = options;

  return (
    <button
      className={cn(css.optionSelect, {
        [css.optionSelectedA]: option === selectedOption,
      })}
      disabled={option === selectedOption}
      onClick={e => onClick({ e, option, value })}
      type="button"
    >
      {option}
    </button>
  );
};

export { OptionButton };
