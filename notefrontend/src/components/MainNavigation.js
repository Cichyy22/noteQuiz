import {
  Box,
  Flex,
  HStack,
  IconButton,
  useDisclosure,
  useColorModeValue,
} from '@chakra-ui/react'
import { NavLink} from 'react-router-dom';
import { HamburgerIcon, CloseIcon } from '@chakra-ui/icons';
import logo from '../idle/LOGO-modified.png';



export default function MainNavigation() {
  const { isOpen, onOpen, onClose } = useDisclosure()

  return (
    <>
    <Box bg={useColorModeValue('gray.100', 'gray.900')} px={4}>
      <Flex h={16} alignItems={'center'} justifyContent={'space-between'}>
        <IconButton
          size={'md'}
          icon={isOpen ? <CloseIcon /> : <HamburgerIcon />}
          aria-label={'Open Menu'}
          display={{ md: 'none' }}
          onClick={isOpen ? onClose : onOpen}
        />
        <HStack spacing={8} alignItems={'center'}>
          <Box>
            <img src={logo} alt="Logo" width={100} height={50} />
          </Box>
          <HStack
            as={'nav'}
            spacing={4}
            display={{ base: 'none', md: 'flex' }}
            className="font-semibold text-gray-800"
          >
            <NavLink key="home" to="/">
              <Box
                px={2}
                py={1}
                rounded={'md'}
                _hover={{
                  textDecoration: 'none',
                  bg: useColorModeValue('gray.200', 'gray.700'),
                  color: 'black',
                }}
                className="hover:text-gray-200"
              >
                Home
              </Box>
            </NavLink>
            <NavLink key="game" to="/game">
              <Box
                px={2}
                py={1}
                rounded={'md'}
                _hover={{
                  textDecoration: 'none',
                  bg: useColorModeValue('gray.200', 'gray.700'),
                  color: 'black',
                }}
                className="hover:text-gray-200"
              >
                Game
              </Box>
            </NavLink>
          </HStack>
        </HStack>
      </Flex>
    </Box>
  </>
  )
}
