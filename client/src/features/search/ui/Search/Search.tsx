import { useState } from 'react';
import cn from 'classnames';
import { Icon } from '~shared/ui/Icon';
import css from './Search.module.scss';
import { SearchResults } from './SearchResults';

const Search = () => {
  const [isExpanded, setIsExpanded] = useState(false);
  const [searchText, setSearchText] = useState('');

  const handleFocus = () => {
    setIsExpanded(true);
  };

  const handleBlur = (event: React.FocusEvent<HTMLInputElement>) => {
    if (!event.relatedTarget || !event.relatedTarget.closest('form')) {
      setIsExpanded(false);
    }
  };

  const handleChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setSearchText(event.target.value);
  };

  const handleFormClose = () => {
    setSearchText('');
    setIsExpanded(false);
  };

  return (
    <form
      className={cn(css.searchForm, {
        [css.expanded]: isExpanded,
      })}
    >
      <label className={css.label}>
        <Icon btnStyle={css.searchIcon} type="search" />
        <input
          className={css.searchInput}
          id="searchInput"
          type="text"
          placeholder="Search.."
          onBlur={handleBlur}
          onFocus={handleFocus}
          value={searchText}
          onChange={handleChange}
        />
        {searchText && (
          <Icon
            btnStyle={css.clearButton}
            onClick={handleFormClose}
            type="close"
          />
        )}
      </label>
      {searchText && (
        <SearchResults
          searchText={searchText}
          className={css.searchResults}
          isExpanded={isExpanded}
          handleFormClose={handleFormClose}
        />
      )}
    </form>
  );
};

export { Search };
