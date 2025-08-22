import { useState, useRef, useEffect } from 'react';
import './App.css';
import {
  Box,
  Container,
  TextField,
  Button,
  Typography,
  Paper,
  AppBar,
  Toolbar,
  IconButton,
  Avatar,
  Card,
  CardContent,
  CircularProgress,
  ThemeProvider,
  createTheme,
  CssBaseline,
} from '@mui/material';
import {
  Send as SendIcon,
  LightMode as LightModeIcon,
  DarkMode as DarkModeIcon,
  Psychology as PsychologyIcon,
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
        main: '#5465FF',
      },
      secondary: {
        main: '#E2E2E2',
      },
      background: {
        default: darkMode ? '#1E1E1E' : '#F7F7F7',
        paper: darkMode ? '#2D2D2D' : '#FFFFFF',
      },
    },
    typography: {
      fontFamily: '"Inter", "Roboto", "Helvetica", "Arial", sans-serif',
    },
    components: {
      MuiCard: {
        styleOverrides: {
          root: {
            borderRadius: '10px',
            boxShadow: darkMode
              ? '0 4px 6px rgba(0, 0, 0, 0.3)'
              : '0 2px 4px rgba(0, 0, 0, 0.05)',
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
          sx={{ borderBottom: '1px solid', borderColor: 'divider' }}
        >
          <Toolbar>
            <PsychologyIcon sx={{ mr: 2, color: 'primary.main' }} />
            <Typography
              variant='h6'
              color='inherit'
              noWrap
              sx={{ flexGrow: 1 }}
            >
              Internal Knowledge Base
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
                  {message.sender === 'ai' && (
                    <Avatar sx={{ bgcolor: 'primary.main', mr: 1 }}>
                      <PsychologyIcon />
                    </Avatar>
                  )}
                  <Card
                    sx={{
                      backgroundColor:
                        message.sender === 'user'
                          ? 'primary.main'
                          : 'background.paper',
                      color:
                        message.sender === 'user' ? 'white' : 'text.primary',
                    }}
                  >
                    <CardContent sx={{ '&:last-child': { pb: 2 } }}>
                      {message.sender === 'ai' ? (
                        <ReactMarkdown>{message.text}</ReactMarkdown>
                      ) : (
                        <Typography>{message.text}</Typography>
                      )}
                      <Typography
                        variant='caption'
                        display='block'
                        sx={{ mt: 1, opacity: 0.7, textAlign: 'right' }}
                      >
                        {message.timestamp.toLocaleTimeString([], {
                          hour: '2-digit',
                          minute: '2-digit',
                        })}
                      </Typography>
                    </CardContent>
                  </Card>
                  {message.sender === 'user' && (
                    <Avatar sx={{ bgcolor: 'grey.400', ml: 1 }}>
                      {/* User's initial or avatar */}U
                    </Avatar>
                  )}
                </Box>
              </Box>
            ))}
            {isLoading && (
              <Box
                sx={{ display: 'flex', justifyContent: 'flex-start', mb: 3 }}
              >
                <Box sx={{ display: 'flex' }}>
                  <Avatar sx={{ bgcolor: 'primary.main', mr: 1 }}>
                    <PsychologyIcon />
                  </Avatar>
                  <Card>
                    <CardContent sx={{ display: 'flex', alignItems: 'center' }}>
                      <CircularProgress size={20} sx={{ mr: 2 }} />
                      <Typography>Thinking...</Typography>
                    </CardContent>
                  </Card>
                </Box>
              </Box>
            )}
            <div ref={messagesEndRef} />
          </Container>
        </Box>

        {/* Input Area */}
        <Paper
          elevation={3}
          sx={{
            p: 2,
            borderTop: '1px solid',
            borderColor: 'divider',
          }}
        >
          <Container maxWidth='md'>
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
                sx={{ mr: 2 }}
              />
              <Button
                variant='contained'
                color='primary'
                endIcon={<SendIcon />}
                onClick={handleSendMessage}
                disabled={isLoading || !input.trim()}
              >
                Send
              </Button>
            </Box>
          </Container>
        </Paper>
      </Box>
    </ThemeProvider>
  );
}

export default App;
