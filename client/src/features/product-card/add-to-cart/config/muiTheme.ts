import createTheme from '@mui/material/styles/createTheme';

export default createTheme({
  components: {
    MuiButton: {
      styleOverrides: {
        root: {
          padding: '21px',
          borderRadius: '8px',
          backgroundColor: '#37643B',
          boxShadow: 'none',
          position: 'relative',

          '&.Mui-disabled': {
            backgroundColor: '#37643B',
          },

          '&:hover': {
            backgroundColor: '#37643B',
            boxShadow: 'none',
          },

          '& svg': {
            position: 'absolute',
          },

          '@media (max-width: 500px)': {
            padding: '13.5px 15px',
            minWidth: '52px',
            borderRadius: '4px',
          },
          '@media (min-width: 1446px)': {
            padding: `${21 / 16}rem ${23 / 16}rem`,
            minWidth: `${65 / 16}rem`,
          },
        },
      },
    },
  },
});
