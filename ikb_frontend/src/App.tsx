import { useState, useRef, useEffect } from 'react';
import './App.css';
import {
  Box,
  Container,
  TextField,
  Button,
  Typography,
  AppBar,
  Toolbar,
  IconButton,
  ThemeProvider,
  createTheme,
  CssBaseline,
  Skeleton,
} from '@mui/material';
import {
  Send as SendIcon,
  LightMode as LightModeIcon,
  DarkMode as DarkModeIcon,
  AutoFixHigh as MagicWandIcon,
} from '@mui/icons-material';
import ReactMarkdown from 'react-markdown';
import axios from 'axios';

// Define message types
interface Message {
  id: string;
  text: string;
  sender: 'user' | 'ai';
  timestamp: Date;
}

function App() {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: '1',
      text: "Hello! I'm your Knowledge Base Assistant. How can I help you today?",
      sender: 'ai',
      timestamp: new Date(),
    },
  ]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [darkMode, setDarkMode] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const theme = createTheme({
    palette: {
      mode: darkMode ? 'dark' : 'light',
      primary: {
        main: '#6366F1', // Indigo
        light: '#818CF8',
        dark: '#4F46E5',
      },
      secondary: {
        main: '#EC4899', // Pink
        light: '#F472B6',
        dark: '#DB2777',
      },
      background: {
        default: darkMode ? '#111827' : '#F9FAFB',
        paper: darkMode ? '#1F2937' : '#FFFFFF',
      },
      error: {
        main: '#EF4444', // Red
      },
      warning: {
        main: '#F59E0B', // Amber
      },
      info: {
        main: '#3B82F6', // Blue
      },
      success: {
        main: '#10B981', // Emerald
      },
    },
    typography: {
      fontFamily: '"Inter", "Roboto", "Helvetica", "Arial", sans-serif',
    },
    components: {
      MuiCard: {
        styleOverrides: {
          root: {
            borderRadius: '12px',
            boxShadow: darkMode
              ? '0 10px 15px -3px rgba(0, 0, 0, 0.3), 0 4px 6px -2px rgba(0, 0, 0, 0.1)'
              : '0 10px 15px -3px rgba(0, 0, 0, 0.05), 0 4px 6px -2px rgba(0, 0, 0, 0.02)',
          },
        },
      },
      MuiButton: {
        styleOverrides: {
          root: {
            borderRadius: '9999px', // Make all buttons circular by default
            textTransform: 'none', // Prevent uppercase text
            fontWeight: 600,
            fontSize: 20,
          },
        },
      },
    },
  });

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const handleSendMessage = async () => {
    if (!input.trim()) return;

    // Add user message
    const userMessage: Message = {
      id: Date.now().toString(),
      text: input,
      sender: 'user',
      timestamp: new Date(),
    };
    setMessages((prev) => [...prev, userMessage]);
    setInput('');
    setIsLoading(true);

    try {
      // Make API call to backend using axios
      const response = await axios.post('http://localhost:3000/v1/chat', {
        prompt: input,
        context: '', // You can add context here if needed
      });

      const data = response.data;

      // Add AI response
      const aiMessage: Message = {
        id: (Date.now() + 1).toString(),
        text: data.message || "I'm sorry, I couldn't process that request.",
        sender: 'ai',
        timestamp: new Date(),
      };
      setMessages((prev) => [...prev, aiMessage]);
    } catch (error) {
      console.error('Error sending message:', error);

      // Get a more specific error message if available
      let errorText =
        'Sorry, there was an error processing your request. Please try again later.';
      if (axios.isAxiosError(error)) {
        if (error.response) {
          // The request was made and the server responded with a status code outside of 2xx range
          errorText = `Error ${error.response.status}: ${
            error.response.data.detail || 'Server error'
          }`;
        } else if (error.request) {
          // The request was made but no response was received
          errorText =
            'No response from server. Please check if the server is running.';
        }
      }

      // Add error message
      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        text: errorText,
        sender: 'ai',
        timestamp: new Date(),
      };
      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Box sx={{ display: 'flex', flexDirection: 'column', height: '100vh' }}>
        {/* App Bar */}
        <AppBar
          position='static'
          color='default'
          elevation={0}
          sx={{
            borderBottom: '1px solid',
            borderColor: 'divider',
            backgroundColor: theme.palette.background.default,
          }}
        >
          <Toolbar>
            <MagicWandIcon sx={{ mr: 2, color: 'primary.main' }} />
            <Typography
              variant='h6'
              color='inherit'
              noWrap
              sx={{ flexGrow: 1 }}
            >
              AdvantaLabs's IKB
            </Typography>
            <IconButton onClick={() => setDarkMode(!darkMode)} color='inherit'>
              {darkMode ? <LightModeIcon /> : <DarkModeIcon />}
            </IconButton>
          </Toolbar>
        </AppBar>

        {/* Chat Messages */}
        <Box
          sx={{
            flexGrow: 1,
            p: 3,
            overflowY: 'auto',
            backgroundColor: theme.palette.background.default,
          }}
        >
          <Container maxWidth='md'>
            {messages.map((message) => (
              <Box
                key={message.id}
                sx={{
                  display: 'flex',
                  justifyContent:
                    message.sender === 'user' ? 'flex-end' : 'flex-start',
                  mb: 3,
                }}
              >
                <Box sx={{ display: 'flex', maxWidth: '80%' }}>
                  <Box
                    sx={{
                      backgroundColor:
                        message.sender === 'user'
                          ? 'linear-gradient(135deg, #FFF6F1 0%, #4F46E5 100%)'
                          : theme.palette.background.default,
                      color:
                        message.sender === 'user' ? 'white' : 'text.primary',
                      borderRadius: 4,
                      backgroundImage:
                        message.sender === 'user'
                          ? 'linear-gradient(135deg, #454545 0%, #5F5f45 100%)'
                          : 'none',
                      boxShadow:
                        message.sender === 'user'
                          ? '0 10px 15px -3px rgba(79, 70, 229, 0.2), 0 4px 6px -2px rgba(79, 70, 229, 0.1)'
                          : '0 10px 15px -3px rgba(0, 0, 0, 0.0), 0 4px 6px -2px rgba(0, 0, 0, 0.0)',
                    }}
                  >
                    <Box>
                      {message.sender === 'ai' ? (
                        <ReactMarkdown>{message.text}</ReactMarkdown>
                      ) : (
                        <Typography sx={{ p: 1.5, whiteSpace: 'collapse' }}>
                          {message.text}
                        </Typography>
                      )}
                    </Box>
                  </Box>
                </Box>
              </Box>
            ))}
            {isLoading && (
              <Box sx={{ display: 'flex', flexDirection: 'column' }}>
                <Skeleton width={300} height={20} />
                <Skeleton width={250} height={20} />
                <Skeleton width={200} height={20} />
                <Box sx={{ display: 'flex', alignItems: 'center', mt: 1 }}>
                  🤔
                </Box>
              </Box>
            )}
            <div ref={messagesEndRef} />
          </Container>
        </Box>

        {/* Input Area */}
        <Box
          sx={{
            width: '100%',
            display: 'flex',
            justifyContent: 'center',
            backgroundColor: theme.palette.background.default,
          }}
        >
          <Container maxWidth='md' sx={{ mb: 10 }}>
            <Box sx={{ display: 'flex', alignItems: 'flex-end' }}>
              <TextField
                fullWidth
                multiline
                maxRows={4}
                placeholder='Ask anything about company policies, procedures, or documentation...'
                variant='outlined'
                value={input}
                onChange={(e: React.ChangeEvent<HTMLInputElement>) =>
                  setInput(e.target.value)
                }
                onKeyDown={handleKeyDown}
                slotProps={{
                  input: {
                    endAdornment: (
                      <Button
                        variant='contained'
                        onClick={handleSendMessage}
                        disabled={isLoading || !input.trim()}
                        sx={{
                          minWidth: '40px',
                          width: '40px',
                          height: '40px',
                          borderRadius: '50%',
                          padding: 0,
                          marginRight: '3px',
                          background:
                            'linear-gradient(135deg, #6366F1 0%, #EC4899 100%)',
                          '&:hover': {
                            background:
                              'linear-gradient(135deg, #4F46E5 0%, #DB2777 100%)',
                            transform: 'translateY(-2px)',
                            boxShadow:
                              '0 10px 25px -5px rgba(99, 102, 241, 0.5), 0 10px 10px -5px rgba(236, 72, 153, 0.3)',
                          },
                          transition: 'all 0.3s ease',
                          display: 'flex',
                          justifyContent: 'center',
                          alignItems: 'center',
                        }}
                      >
                        <SendIcon sx={{ color: 'white', fontSize: '1.2rem' }} />
                      </Button>
                    ),
                  },
                }}
                sx={{
                  width: '100%',
                  '& .MuiOutlinedInput-root': {
                    borderRadius: '30px',
                    paddingRight: '8px',
                    backgroundColor: darkMode
                      ? 'rgba(31, 41, 55, 0.7)'
                      : 'rgba(249, 250, 251, 0.7)',
                    '&:hover .MuiOutlinedInput-notchedOutline': {
                      borderColor: theme.palette.primary.light,
                    },
                    '&.Mui-focused .MuiOutlinedInput-notchedOutline': {
                      borderColor: theme.palette.primary.main,
                      borderWidth: '2px',
                    },
                  },
                  '& .MuiOutlinedInput-notchedOutline': {
                    borderColor: darkMode
                      ? 'rgba(75, 85, 99, 0.5)'
                      : 'rgba(209, 213, 219, 0.8)',
                  },
                }}
              />
            </Box>
          </Container>
        </Box>
      </Box>
    </ThemeProvider>
  );
}

export default App;
