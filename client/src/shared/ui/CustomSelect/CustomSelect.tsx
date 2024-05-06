import { FC, useState } from 'react';
import { useSearchParams } from 'react-router-dom';

import cn from 'classnames';

import { type TSortBy } from '~entities/product';
import { getSearchWith } from '~shared/lib/getSearchWith';
import { useToggle } from '~shared/model/useToggle';

import { OptionButton } from './ui/OptionButton';
import { THandleOption } from './types/THandleOption';

import css from './CustomSelect.module.scss';

type TCustomSelectProps = {
  options: TSortBy;
  startValue: string;
};

const CustomSelect: FC<TCustomSelectProps> = ({ options, startValue }) => {
  const [searchParams, setSearchParams] = useSearchParams();
  const [isModalOpen, toggle] = useToggle();
  const [selectedOption, setSelectedOption] = useState(startValue);

  const handleOption = ({ e, option, value }: THandleOption) => {
    e.stopPropagation();

    const search = getSearchWith({ sortBy: value }, searchParams);

    setSearchParams(search);

    setSelectedOption(option);
    toggle();
  };

  return (
    <div
      className={css.containerSelect}
      tabIndex={-1}
      role="button"
      onClick={toggle}
      onKeyDown={() => {}}
    >
      <div className={cn(css.lableName)}>
        {selectedOption}
        <svg
          className={cn(css.arrow, {
            [css.isArrowRotate]: isModalOpen,
          })}
          width="24"
          height="24"
          viewBox="0 0 24 24"
          fill="none"
          xmlns="http://www.w3.org/2000/svg"
        >
          <path
            // eslint-disable-next-line max-len
            d="M20.1126 16.7283C20.208 16.8185 20.3203 16.8891 20.4431 16.9359C20.5658 16.9827 20.6965 17.0049 20.8278 17.0012C20.9591 16.9975 21.0884 16.9679 21.2083 16.9142C21.3282 16.8606 21.4363 16.7838 21.5266 16.6883C21.6168 16.5928 21.6873 16.4805 21.7341 16.3578C21.7809 16.2351 21.8031 16.1043 21.7994 15.973C21.7957 15.8417 21.7662 15.7124 21.7125 15.5926C21.6588 15.4727 21.582 15.3645 21.4866 15.2743L12.4866 6.77432C12.3009 6.59878 12.0551 6.50098 11.7996 6.50098C11.544 6.50098 11.2982 6.59878 11.1126 6.77432L2.11156 15.2743C2.014 15.3639 1.93521 15.4721 1.87979 15.5924C1.82436 15.7127 1.7934 15.8428 1.7887 15.9752C1.78399 16.1076 1.80564 16.2396 1.85239 16.3636C1.89914 16.4876 1.97005 16.601 2.061 16.6973C2.15195 16.7936 2.26114 16.8709 2.38222 16.9247C2.50329 16.9785 2.63385 17.0076 2.76629 17.0105C2.89874 17.0134 3.03044 16.9899 3.15374 16.9415C3.27705 16.8931 3.38949 16.8206 3.48456 16.7283L11.7996 8.87632L20.1126 16.7283Z"
            fill="#A0A0A0"
          />
        </svg>

        <div className={css.arrowsMob}>
          <svg
            className={cn(css.arrowsMobUp, {
              [css.isMobailArrowRotateDown]: isModalOpen,
            })}
            width="10"
            height="16"
            viewBox="0 0 10 16"
            fill="none"
            xmlns="http://www.w3.org/2000/svg"
          >
            <path d="M9 11L5 15L1 11H9ZM5 15V1V15Z" fill="#A0A0A0" />
            <path
              d="M5 15L9 11H1L5 15ZM5 15V1"
              stroke="#A0A0A0"
              strokeWidth="1.5"
              strokeLinecap="round"
              strokeLinejoin="round"
            />
          </svg>
          <svg
            className={cn(css.arrowsMobDown, {
              [css.isMobailArrowRotateUp]: isModalOpen,
            })}
            width="10"
            height="16"
            viewBox="0 0 10 16"
            fill="none"
            xmlns="http://www.w3.org/2000/svg"
          >
            <path d="M9 11L5 15L1 11H9ZM5 15V1V15Z" fill="#A0A0A0" />
            <path
              d="M5 15L9 11H1L5 15ZM5 15V1"
              stroke="#A0A0A0"
              strokeWidth="1.5"
              strokeLinecap="round"
              strokeLinejoin="round"
            />
          </svg>
        </div>
      </div>
      <div
        className={cn(css.menuSelect, {
          [css.open]: isModalOpen,
        })}
      >
        {options.map(option => (
          <OptionButton
            key={option[0]}
            onClick={handleOption}
            options={option}
            selectedOption={selectedOption}
          />
        ))}
      </div>
    </div>
  );
};

export { CustomSelect };
